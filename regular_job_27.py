from classes.ForecastModel import ForecastModel
fm = ForecastModel(27)
fm.train()
fm.todb(all=True)

# from classes.RegularJob import RegularJob

# job = RegularJob()

# if job.check_date():
#     if job.check_real():
#         if job.check_training(27):
#             job.check_predicting(27)