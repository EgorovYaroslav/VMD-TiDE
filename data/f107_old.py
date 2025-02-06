import pandas as pd
import functions.db as db
import requests
from scipy.signal import savgol_filter
from datetime import datetime



def get_train_data(db_name='data3',smooth=0, cutoff = datetime.today().strftime('%Y-%m-%d')):
    df = pd.read_csv('data/data_f107_v2.csv', header=0, index_col = 'date', parse_dates=True)
    df['date'] = df.index
    df['real'] = df.adj
    df.drop('ssn', axis=1, inplace=True)
    df.drop('stdd', axis=1, inplace=True)
    df.drop('adj', axis=1, inplace=True)

    df2= db.select_rows(f"SELECT date,real FROM {db_name} where date > '2024-06-19' and real <> 'NaN' order by date")
    df2 = df2.set_index('date')
    df2['date'] = df2.index
    df2
    df = pd.concat([df, df2])
    df.loc[df.real==0, 'real'] = None
    df.loc[df.real>350, 'real'] = None
    df.loc[df.real<60, 'real'] = None
    df.real = df.real.interpolate(method='linear')
    df.real.values[0] = df.real.values[1]
    df.date = df.date.astype('datetime64[ns]')
    df.index = df.date
    if smooth>0:
        df['real'] = savgol_filter(df['real'], smooth, 3)
    df = df[df.date<pd.to_datetime(cutoff)]

    return df

def get_db_data(db_name='data3',smooth=0):
    df = db.select_rows(f"SELECT date,real FROM {db_name} where real <> 'NaN' and date > '2023-01-01' order by date")
    df = df.set_index('date')
    df['date'] = df.index
    if smooth>0:
        df['real'] = savgol_filter(df['real'], smooth, 3)
    return df

def get_eval_data(db_name='data3',date_range=[25,25]):
    df = get_train_data(db_name)
    date_range = ['2024-01-01','2024-01-02']
    if all(isinstance(x, int) for x in date_range):
        date_range = get_solar_cycle_range(date_range)
    df = df[df.date>=date_range[0]]
    df = df[df.date<=date_range[1]]
    return df

def get_solar_cycle_range(date_range):
    df = db.select_rows(f"SELECT * FROM solar_cycles where name in ({date_range[0]},{date_range[1]})")
    return [df.starts.min(),df.ends.max()]


def get_new_request(date):
    url = ('http://10.0.3.233:8000/F107/get_latest_F107')
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        data = response.json()
        if data['mes_date'] == date:
            return data['f']
        else:
            return False
    except (requests.exceptions.RequestException, StopIteration):
        return False

def get_request(date, mode='nowcast'):
    url = ('http://10.0.3.233:8000/F107/get_data?'
        f'start_date={date}T00:00&end_date={date}T23:00&F107_stage_enum={mode}')
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        data = response.json()
        if data[-1]['f'] == "nan":
            return False
        else:
            return data[-1]['f']
    except (requests.exceptions.RequestException, StopIteration):
        return False