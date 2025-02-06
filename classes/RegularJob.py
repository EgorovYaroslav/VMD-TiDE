import functions.db as db
from classes.ForecastModel import ForecastModel
import functions.utilites as util
from datetime import datetime

class RegularJob:
    def __init__(
        self,
        **kwargs
    ):
        self.today = datetime.now().date()

    def check_date(self):
        df = db.select_rows("select * from jobs")
        if df.date[0] < self.today:
            db.update_row(f"UPDATE jobs SET date='{self.today}', real=False, train_7=False, train_27=False, predict_7=False, predict_27=False, decomposed=False")


    def check_real(self):
        df = db.select_rows("select * from jobs")
        if df.real[0]:
            return True
        else:
            if util.check_new_real():
                fm = ForecastModel(7)
                fm.prepare_data_decomposed()
                db.update_row("UPDATE jobs SET real=True, decomposed=True")
            return False

    def check_training(self, prediction_length):
        df = db.select_rows("select * from jobs")
        if not df[f'train_{prediction_length}'][0]:
            fm = ForecastModel(prediction_length)
            fm.train()
            db.update_row(f"UPDATE jobs SET train_{prediction_length}=True")
            return True
        else:
            return True

    def check_predicting(self, prediction_length):
        df = db.select_rows("select * from jobs")
        if not df[f'predict_{prediction_length}'][0]:
            fm = ForecastModel(prediction_length, mode='forecast')
            fm.todb()
            db.update_row(f"UPDATE jobs SET predict_{prediction_length}=True")
            return False
        return True