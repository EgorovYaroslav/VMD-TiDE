import functions.utilites as util
from classes.ForecastModel import ForecastModel
if util.check_new_real():
    fm = ForecastModel(7)
    fm.prepare_data_decomposed()