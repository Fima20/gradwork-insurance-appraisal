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


def calc_coefficient_insurance():
    pass


def calc_recommended_coefficient_insurance(min_allowable_income: float,
                                           budget_lesion_prediction: [float],
                                           sum_contracts_prediction: [float]):

    coefficient = ((min_allowable_income + sum(budget_lesion_prediction)) / sum(sum_contracts_prediction)) * 12
    return coefficient


def forecasting(capital_lesion: [float],
                sum_contracts: [float],
                last_budget: float,
                PERIOD_PREDICTION_MONTH: int = 12,
                SMOOTH_INTER: int = 3,
                KF: float = 0.004254,
                PERIOD_WORK_MONTH: int = None):

    if PERIOD_WORK_MONTH:
        pass
    elif len(capital_lesion) > len(sum_contracts):
        PERIOD_WORK_MONTH = int(len(sum_contracts))
    else:
        PERIOD_WORK_MONTH = int(len(capital_lesion))

    sum_contracts = sum_contracts[-PERIOD_WORK_MONTH:-1]
    capital_lesion = capital_lesion[-PERIOD_WORK_MONTH:-1]

    #smooth_capital_lesion = smoothing_middle(capital_lesion, SMOOTH_INTER)
    #budget_lesion_prediction = model_arima(smooth_capital_lesion, PERIOD_PREDICTION_MONTH)
    budget_lesion_prediction = lesion_prediction(capital_lesion, PERIOD_PREDICTION_MONTH)
    #budget_lesion_prediction = model_arima(capital_lesion, PERIOD_PREDICTION_MONTH)

    smooth_sum_contracts = smoothing_middle(sum_contracts, SMOOTH_INTER)
    sum_contracts_prediction = model_holt_winters(smooth_sum_contracts, PERIOD_PREDICTION_MONTH)

    res_budget = [last_budget]
    for iter in range(PERIOD_PREDICTION_MONTH):
        diff_budget_income = sum_contracts_prediction[iter] * KF / 12
        #diff_budget_income = sum_contracts_prediction[iter] * KF
        res_budget.append(res_budget[iter] + diff_budget_income - budget_lesion_prediction[iter])

    return res_budget, budget_lesion_prediction, sum_contracts_prediction


def lesion_prediction(lesion, PERIOD_PREDICTION_MONTH):
    res = []
    lesion = lesion[-15:-1]
    len_lesion = len(lesion)
    for iter in range(PERIOD_PREDICTION_MONTH):
        if iter >= len_lesion:
            cout = iter % len_lesion
        else:
            cout = iter
        print(iter, len_lesion, cout)
        res.append(lesion[cout])
    return res

