import psycopg2
import psycopg2.extras
from dotenv import dotenv_values
from psycopg2 import sql
from contextlib import closing
import sqlalchemy

import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)
register_adapter(np.int32, addapt_numpy_int32)
register_adapter(np.ndarray, addapt_numpy_array)

def get_row(query):
    config = dotenv_values(".env")
    with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
            cursor.execute(query)
            row = cursor.fetchone()
    return row


def num_rows(yht):
    import functions.db as db
    res = db.get_row("SELECT count(*) FROM results WHERE yht='"+str(yht)+"'")
    return res.count

def get_rows(query):
    config = dotenv_values(".env")

    with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
            cursor.execute(query)
            row = cursor.fetchall()
    return row


def select_rows(query):
    import pandas as pd
    config = dotenv_values(".env")

    conn = psycopg2.connect("host='{}' dbname='{}' user={} password={}".format(
        config['db_host'], config['db_database'], config['db_user'], config['db_password']))
    dat = pd.read_sql_query('SET search_path TO "'+str(config['db_schema'])+'"; '+query, conn)
    conn = None

    return dat


def update_row(query):
    config = dotenv_values(".env")
    with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            conn.autocommit = True
            cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
            cursor.execute(query)


def add_result(name, values):
    config = dotenv_values(".env")
    with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
            insert = sql.SQL('INSERT INTO '+str(name)+' (date_obs, phi, lamda, yht, pair,params,start_date) VALUES ({})').format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)


def add_row(name, values):
    config = dotenv_values(".env")
    with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
            insert = sql.SQL('INSERT INTO '+str(name)+' VALUES (DEFAULT,{})').format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)

def insert_df_rows(name, df):

    if len(df) > 0:
        config = dotenv_values(".env")
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        #create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(name,columns,values)

        with closing(psycopg2.connect(dbname=config['db_database'], user=config['db_user'],
                                  password=config['db_password'], host=config['db_host'])) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL('SET search_path TO "'+str(config['db_schema'])+'"'))
                psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
                conn.commit()
                cursor.close()

def insert_df(name, df):
    # create a connection to the database
    engine = sqlalchemy.create_engine('postgresql://postgres:asd123fgh@localhost:5432/postgres',
        connect_args={'options': '-csearch_path={}'.format('f107')})

    # write the DataFrame to the database
    df.to_sql(name, engine, if_exists='replace', index=True)