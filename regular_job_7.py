from classes.ForecastModel import ForecastModel
from functions.utilites import log_message
from datetime import datetime


log_message('Start Training 7-day horizon')

fm = ForecastModel(7, context_length=126, tuned='default', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'])
fm.train()
fm = ForecastModel(7, context_length=126, tuned='default', data_range=['2023-01-01',datetime.today().strftime('%Y-%m-%d')])
fm.todb(all=True)

log_message('Training 7-day horizon has been finished')