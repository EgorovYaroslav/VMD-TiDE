from classes.ForecastModel import ForecastModel
fm = ForecastModel(7, context_length=126, tuned='default', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'], device='cuda')
fm.train()