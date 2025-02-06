from classes.ForecastModel import ForecastModel
fm = ForecastModel(7)
fm.train()
fm.todb(all=True)
# import functions.utilites as util
# from classes.ForecastModel import ForecastModel
# if util.check_new_real():
#     fm = ForecastModel(7)
#     fm.prepare_data_decomposed()
#     fm.todb(all=True)
#     fm = ForecastModel(27)
#     fm.todb(all=True)

# from classes.RegularJob import RegularJob

# job = RegularJob()

# if job.check_date():
#     if job.check_real():
#         if job.check_training(7):
#             job.check_predicting(7)