from classes.ForecastModel import ForecastModel
from datetime import datetime
fm = ForecastModel(27,context_length=27, tuned='default', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'])
fm.train()
fm = ForecastModel(27, context_length=27, tuned='default', data_range=['2023-01-01',datetime.today().strftime('%Y-%m-%d')])
fm.todb(all=True)

# from classes.RegularJob import RegularJob

# job = RegularJob()

# if job.check_date():
#     if job.check_real():
#         if job.check_training(27):
#             job.check_predicting(27)