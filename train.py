from classes.ForecastModel import ForecastModel
fm = ForecastModel(7, context_length=126, tuned='default', split_date='1986-09-01', data_range=['1954-01-01', '2008-12-31'], device='cuda')
fm.train()

"t1(id INT, date TIMESTAMP, real FLOAT, crn FLOAT, cycle_day_number FLOAT, sdn FLOAT, IMF1 FLOAT, IMF2 FLOAT, IMF3 FLOAT, R FLOAT, IMF1_1 FLOAT, IMF1_2 FLOAT, IMF1_3 FLOAT, IMF2_1 FLOAT, IMF2_2 FLOAT, IMF2_3 FLOAT, IMF3_1 FLOAT, IMF3_2 FLOAT, IMF3_3 FLOAT, R_1 FLOAT, R_2 FLOAT, R_3 FLOAT)"