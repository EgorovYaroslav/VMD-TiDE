# from classes.ForecastModelTest2 import ForecastModel
# fm = ForecastModel(7, context_length=126, alias='cov', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'])

# from classes.ForecastModelTest12 import ForecastModel
# fm = ForecastModel(7, alias='nocov', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'])

from classes.ForecastModel30 import ForecastModel
fm = ForecastModel(7, context_length=126, tuned='default', alias='f30', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'])

fm.train()
# fm.todb(all=True)

