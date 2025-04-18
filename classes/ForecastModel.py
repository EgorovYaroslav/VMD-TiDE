import functions.db as db
from classes.TideModel import TideModel
from datetime import datetime
from datetime import timedelta
import functions.utilites as util
# import numpy as np
from vmdpy import VMD
import pandas as pd
from darts import TimeSeries
from darts.metrics.metrics import mape, mae, rmse, smape


class ForecastModel:
    def __init__(
        self,
        prediction_length,
        context_length = 0,
        alias='',
        tuned='default',
        data_range = ['1954-01-01', datetime.today().strftime('%Y-%m-%d')],
        past_covariates=['sdn'],
        future_covariates=['crn'],
        split_date = '2008-12-01',
        **kwargs
    ):
        self.context_length = context_length
        self.prediction_length = prediction_length
        self.tuned = tuned
        self.past_covs = past_covariates
        self.future_covs = future_covariates
        self.alias = alias
        self.data_range = data_range
        self.split_date = split_date
        # self.model_name = f'adj_{tuned}_'
        self.modes = ['IMF1_1', 'IMF2_1', 'IMF3_1', 'IMF1_2', 'IMF2_2', 'IMF3_2', 'IMF1_3', 'IMF2_3', 'IMF3_3', 'R_1', 'R_2', 'R_3']

    def get_solar_cycle_range(self, date_range):
        df = db.select_rows(f"SELECT * FROM solar_cycles where name in ({date_range[0]},{date_range[1]})")
        return [df.starts.min(),df.ends.max()]

    def get_data(self, table='data', decompose=False):
        data_range = self.data_range
        if decompose:
            data_range[0] = '1954-01-01'
        if all(isinstance(x, int) for x in data_range):
            data_range = self.get_solar_cycle_range(data_range)

        df = db.select_rows(f"SELECT * from {table} WHERE date between '{data_range[0]}' and '{data_range[1]}' order by date")
        df.date = df.date.astype('datetime64[ns]')
        df.index = df.date
        return df

    def add_future_points_to_df(self, df):
        # df['date'] = df['date'].astype('datetime64[ns]')
        date_range = pd.date_range(df.date.max(), df.date.max() + timedelta(self.prediction_length))
        df1 = pd.DataFrame(
            {'date': date_range,
            'real': 0.0,
            # 'IMF1': 0.0,
            # 'IMF2': 0.0,
            # 'IMF3': 0.0,
            # 'Residuals': 0.0,
            'crn': util.convert_date_to_crn(date_range),
            'sdn': util.convert_dates_to_cycle_day_with_cycle_number(list(date_range.strftime('%Y-%m-%d'))),
        })
        for imf in self.modes:
            df1[imf] = 0.0
        df = pd.concat([df, df1[1:]])
        df.date = df.date.astype('datetime64[ns]')
        df.index = df.date
        return df

    def vmd_decompose(self, df, alpha=2626, tau=0, K=3, DC=0, init=1, tol=1e-7):
        f = df.real.values
        #. some sample parameters for VMD
        # alpha = 2626       # moderate bandwidth constraint
        # tau = 0.            # noise-tolerance (no strict fidelity enforcement)
        # K = 3              # 3 modes
        # DC = 0             # no DC part imposed
        # init = 1           # initialize omegas uniformly
        # tol = 1e-7
        #. Run VMD
        u, u_hat, omega = VMD(f, alpha, tau, K, DC, init, tol)
        check_shape = f.shape[0]==u.T.shape[0]
        # residuals = f-np.sum(u.T, axis=1) if check_shape else f[1:]-np.sum(u.T, axis=1)

        column_headers = ['IMF1', 'IMF2', 'IMF3']
        # residuals = residuals[:, np.newaxis]
        # result = np.hstack(u.T)
        df2 = pd.DataFrame(u.T, columns=column_headers)
        df2.index = df.index if check_shape else df.index[1:]

        return pd.merge(df, df2, left_index=True, right_index=True)

    def prepare_data_decomposed(self):
        df = self.get_data(decompose=True)
        df = self.vmd_decompose(df)
        df['R'] = df.real - df.IMF1 - df.IMF2 - df.IMF3

        df.reset_index(drop=True, inplace=True)
        df.index = df.id
        df.drop('id', axis=1, inplace=True)
        df.drop_duplicates(subset=['date'],keep='last', inplace=True)

        imfs = ['IMF1', 'IMF2', 'IMF3', 'R']
        for imf in imfs:
            df2 = df[['date',imf]]
            df2.columns = ['date', 'real']
            df2 = self.vmd_decompose(df2)
            df[f'{imf}_1'] = df2['IMF1']
            df[f'{imf}_2'] = df2['IMF2']
            df[f'{imf}_3'] = df2['IMF3']
        # return df
        db.insert_df('data_decomposed_twice', df)

    def process_data(self, mode="train", table='data_decomposed_twice'):
        df = self.get_data(table=table)
        if mode == 'forecast':
            df = self.add_future_points_to_df(df)
        return df

    def prepare_model(self, df, imf, mode='train'):
        model_name = f'{self.alias}_adj_{self.tuned}_{imf}'
        return TideModel(df, self.context_length, self.prediction_length, model_name=model_name, target=imf, tuned = self.tuned,past_covariates=self.past_covs, future_covariates=self.future_covs, mode=mode, split_date = self.split_date)

    def train(self):
        df = self.process_data()
        for imf in self.modes:
            model = self.prepare_model(df, imf)
            model.train()

    def train_imf(self, imf):
        df = self.process_data(table='data_decomposed_twice')
        model = self.prepare_model(df, imf)
        model.train()

    def forecast(self, mode='forecast'):
        df = self.process_data(mode=mode)
        for imf in self.modes:
            model = self.prepare_model(df, imf, mode=mode)
            pred, ans = model.predict_all()
            if imf == self.modes[0]:
                predictions = pred.pd_dataframe()
                answers = ans.pd_dataframe()
            else:
                # predictions = predictions.concatenate(pred,axis=1)
                # answers = answers.concatenate(ans,axis=1)
                predictions = pd.concat([predictions,pred.pd_dataframe()],axis=1)
                answers = pd.concat([answers,ans.pd_dataframe()],axis=1)
        predictions = predictions.dropna()
        predictions['date'] = predictions.index
        predictions = TimeSeries.from_dataframe(predictions, 'date', self.modes)
        answers = answers.dropna()
        answers['date'] = answers.index
        answers = TimeSeries.from_dataframe(answers, 'date', self.modes)


        return predictions.sum(axis=1), answers.sum(axis=1)

    def make_prediction(self):
        df = self.process_data(mode='forecast')
        for imf in self.modes:
            model = self.prepare_model(df, imf, mode='forecast')
            pred = model.predict()
            if imf == self.modes[0]:
                predictions = pred.pd_dataframe()
            else:
                predictions = pd.concat([predictions,pred.pd_dataframe()],axis=1)
        predictions = predictions.dropna()
        predictions['date'] = predictions.index
        predictions = TimeSeries.from_dataframe(predictions, 'date', self.modes)
        return predictions.sum(axis=1)


    def evaluate(self):

        predictions, answers = self.forecast()
        print("Evaluation Metrics:")
        print(f"RMSE: {rmse(answers, predictions):.3f}")
        print(f"SMAPE: {smape(answers, predictions):.3f}")
        print(f"MAPE: {mape(answers, predictions):.3f}")
        print(f"MAE: {mae(answers, predictions):.3f}")

    def evaluate_todb(self, cycle_number):
        predictions, answers = self.forecast(mode='evaluate')
        db.add_row('comparison', [self.alias, self.context_length, self.prediction_length, rmse(answers, predictions),mape(answers, predictions),mae(answers, predictions),smape(answers, predictions), cycle_number])

    def todb(self, all=False):
        if all:
            predictions, answers = self.forecast()
        else:
            predictions = self.make_prediction()
        horizon = self.prediction_length
        results = predictions.pd_dataframe().set_axis(['value'], axis=1)
        results['date'] = results.index
        results.reset_index(drop=True, inplace=True)
        results.index = results.index + 1
        results = results.reindex(columns=['date', 'value'])
        if all:
            db.insert_df(f'forecast_{horizon}', results)
        else:
            # results['index'] = results.index
            db.insert_df_rows(f'forecast_{horizon}', results.tail(1))
