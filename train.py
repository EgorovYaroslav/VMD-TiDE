from classes.ForecastModel import ForecastModel
fm = ForecastModel(27)
fm.prepare_data_decomposed()
fm.train()
fm.todb(all=True)

