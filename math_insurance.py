import numpy as np
import statsmodels
from statsmodels.tsa.holtwinters import ExponentialSmoothing, Holt, SimpleExpSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


def middle_value(data_list, step):
    res = []
    for iter in range(int(len(data_list)/step)):
        res.append(sum([data_list[iter*step+i] for i in range(step)])/step)
    return res


# def smoothing_middle(data_list, step):
#     res = []
#     for i in range(step):
#         data_list.insert(0, data_list[0])
#     for num, iter in enumerate(data_list, 0):
#         res.append(sum(data_list[num:num+step])/step)
#
#     return res

def smoothing_middle(data_list, step, cycle=2):

    for c in range(cycle):

        for i in range(step):
            data_list.insert(0, data_list[0])
        res = []
        for num in range(len(data_list)):
            res.append(sum(data_list[num:num+step])/len(data_list[num:num+step]))
        data_list = res[step:]

    return data_list


def moving_average(a, n=3, post_mode=False):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    res = ret[n - 1:] / n
    if post_mode:
        return res[0:-1]
    else:
        return np.concatenate(([0]*(len(a)-len(res)), res))


def holt_winters(df, period):
    model_holt = ExponentialSmoothing(endog=df, trend="add", seasonal="add", seasonal_periods=3).fit()
    predictions = model_holt.forecast(steps=period)
    return [x for x in predictions]


def arima_model(data_list, period, p=3, q=0, d=4):
    model = ARIMA(data_list, order=(p, q, d))
    model_fit = model.fit()
    return model_fit.predict()[0:period]


def sarimax(data_list, period):
    model = SARIMAX(data_list, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(period)
    return yhat[0:period]
    # return [i*-1 for i in yhat[0:period]]
