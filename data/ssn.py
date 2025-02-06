import pandas as pd
import functions.db as db
import requests
from scipy.signal import savgol_filter
def get_train_data(db_name,smooth=0):
    df = pd.read_csv('data/spotfull.csv', header=0, index_col = 'date', parse_dates=True)
    df['date'] = df.index
    df['real'] = df.real

    df2= db.select_rows(f"SELECT date,real FROM {db_name} where date > '2024-06-27' and real <> 'NaN' order by date")
    df2 = df2.set_index('date')
    df2['date'] = df2.index
    df2
    df = pd.concat([df, df2])
    df.loc[df.real==0, 'real'] = None
    # df.loc[df.real>350, 'real'] = None
    # df.loc[df.real<60, 'real'] = None
    df.real = df.real.interpolate(method='linear')
    df.real.values[0] = df.real.values[1]
    df.date = df.date.astype('datetime64[ns]')
    df.index = df.date
    if smooth>0:
        df['real'] = savgol_filter(df['real'], smooth, 3)
    return df

def get_db_data(db_name,smooth=0):
    df = db.select_rows(f"SELECT date,real FROM {db_name} where real <> 'NaN' order by date")
    df = df.set_index('date')
    df['date'] = df.index
    if smooth>0:
        df['real'] = savgol_filter(df['real'], smooth, 3)
    return df

def get_eval_data(db_name,cycle_number):
    df = get_train_data(db_name)
    cycle = get_solar_cycle_range(cycle_number[0],cycle_number[1])
    df = df[df.date>=cycle[0]]
    df = df[df.date<=cycle[1]]
    return df

def get_solar_cycle_range(start,end):
    """
    Returns a list of two dates, which represent the start and end of the given solar cycles.

    Parameters
    ----------
    start : int
        The start solar cycle number.
    end : int
        The end solar cycle number.

    Returns
    -------
    list
        A list of two strings, which represent the start and end dates of the given solar cycles.
    """
    cycles = {
        19: ['1954-04-01','1964-10-01'],
        20: ['1964-10-01','1976-03-01'],
        21: ['1976-03-01','1986-09-01'],
        22: ['1986-09-01','1996-08-01'],
        23: ['1996-08-01','2008-12-01'],
        24: ['2008-12-01','2019-12-01'],
        25: ['2019-12-01','2025-07-01']
    }
    return [cycles[start][0],cycles[end][1]]

def get_request(date, mode='daily'):
    url = ('http://10.0.3.233:8000/sun/get_spot_data_range?'
        f'start_date={date}&end_date={date}&spot_stage_enum={mode}')
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        data = response.json()
        value = next(iter(data.values()))
        if value == 'NaN':
            return False
        else:
            return value
    except (requests.exceptions.RequestException, StopIteration):
        return False