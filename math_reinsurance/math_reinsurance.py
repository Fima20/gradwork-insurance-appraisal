import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing, Holt, SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


def smoothing_middle(data_list, step, cycle=2):
    for c in range(cycle):

        for i in range(step):
            data_list.insert(0, data_list[0])
        res = []
        for num in range(len(data_list)):
            res.append(sum(data_list[num:num + step]) / len(data_list[num:num + step]))
        data_list = res[step:]

    return data_list


def moving_average(a, n=3, post_mode=False):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    res = ret[n - 1:] / n
    if post_mode:
        return res[0:-1]
    else:
        return np.concatenate(([0] * (len(a) - len(res)), res))


def model_holt_winters(df, period):
    model_holt = ExponentialSmoothing(endog=df, trend="add", seasonal="add", seasonal_periods=3).fit()
    predictions = model_holt.forecast(steps=period)
    return [x for x in predictions]


def model_arima(data_list, period, p=3, q=0, d=4):
    model = ARIMA(data_list, order=(p, q, d))
    model_fit = model.fit()
    return model_fit.predict()[0:period]

min_allowable_income: float = 1000000


def forecasting(capital_lesion: [int],
                sum_contracts: [int],
                last_budget: float,
                PERIOD_PREDICTION_MONTH: int = 12,
                SMOOTH_INTER: int = 3,
                KF: float = 0.004254,
                PERIOD_WORK_MONTH: int = None):

    if PERIOD_WORK_MONTH:
        pass
    elif len(capital_lesion) > len(sum_contracts):
        PERIOD_WORK_MONTH = len(sum_contracts)
    else:
        PERIOD_WORK_MONTH = len(capital_lesion)

    sum_contracts = sum_contracts[-PERIOD_WORK_MONTH, -1]
    capital_lesion = capital_lesion[-PERIOD_WORK_MONTH, -1]

    smooth_capital_lesion = smoothing_middle(capital_lesion, SMOOTH_INTER)
    budget_lesion_prediction = model_arima(smooth_capital_lesion, PERIOD_PREDICTION_MONTH)

    smooth_sum_contracts = smoothing_middle(sum_contracts, SMOOTH_INTER)
    sum_contracts_prediction = model_holt_winters(smooth_sum_contracts, PERIOD_PREDICTION_MONTH)

    res_budget = [last_budget]
    for iter in range(PERIOD_PREDICTION_MONTH):
        diff_budget_income = sum_contracts_prediction[iter] * KF / 12
        res_budget.append(res_budget[iter] + diff_budget_income - budget_lesion_prediction[iter])

    return res_budget
