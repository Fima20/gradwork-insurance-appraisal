import example
import matplotlibgraph
import math_insurance
import pandas as pd
import numpy as np
from company_model import TypeInsurance, Contract, SimulatorInsurance
from example import OSAGO, KASKO
import random

if __name__ == '__main__':

    period = 6

    def create_contracts_two_year(object_SimulatorInsurance, object_TypeInsurance):
        object_SimulatorInsurance.list_TypeInsurance.append(object_TypeInsurance)
        object_SimulatorInsurance.create_contracts(object_TypeInsurance=object_SimulatorInsurance.list_TypeInsurance[0],
                                                   num_contracts=random.randint(1000, 10000),
                                                   timestamp_from_from_=-24,
                                                   timestamp_from_to_=48)


    def create_contracts_uni(object_SimulatorInsurance, object_TypeInsurance, year=5):
        object_SimulatorInsurance.list_TypeInsurance.append(object_TypeInsurance)
        object_SimulatorInsurance.create_contracts(object_TypeInsurance=object_SimulatorInsurance.list_TypeInsurance[0],
                                                   num_contracts=random.randint(1000*year, 5000*year),
                                                   timestamp_from_from_=-12*year,
                                                   timestamp_from_to_=24*year)

    def insurance_first(timestamp=24):
        sim = SimulatorInsurance(time_mode=True)
        create_contracts_two_year(sim, OSAGO)
        #Company_budget_diff_, Company_budget_ = sim.simulator_period_random(24)
        Company_budget_income_, Company_budget_lesion_, Company_budget_ = sim.simulator_period_trend(to_=timestamp, trend=example.example_trend_2)

        for i in sim.list_Contracts:
            print(i.sum, i.price*12, i.price)
        print(len(sim.list_Contracts))
        print(Company_budget_income_)
        print(Company_budget_lesion_)
        print(Company_budget_)
        print(Company_budget_[-1])

        matplotlibgraph.simple_graph([Company_budget_], range(timestamp+1))
        # matplotlibgraph.plotly_df(Company_budget_)

    def insurance_method(timestamp=24):

        sim = SimulatorInsurance(time_mode=True)
        create_contracts_uni(sim, OSAGO, year=period)
        Company_budget_income_, Company_budget_lesion_, Company_budget_, Sum_contracts_ = sim.simulator_period_trend(to_=timestamp, trend=example.example_trend_4)

        Company_budget_lesion_ = [x * (-1) for x in Company_budget_lesion_]

        # for i in sim.list_Contracts:
        #     print(i.sum, i.price*12, i.price)
        # print(len(sim.list_Contracts))
        # print(Company_budget_income_)
        # print(Company_budget_lesion_)
        # print(Company_budget_)
        print(Company_budget_[-1])

        def method_first():
            """
            budget_les_pr - 0-72 с прогнозом
            predictions_rolling_mean - сглаженый прогноз 60-72
            budget_rolling_mean - сглаженый бюджет
            """

            # budget_les_pr = [0] + Company_budget_lesion_[0:60] + holt_winters.prediction(Company_budget_lesion_[0:60], 12)
            budget_les_pr = [0] + Company_budget_lesion_[0:60] + math_insurance.holt_winters(math_insurance.moving_average(Company_budget_lesion_[0:60], n=4, zero_mode=True), 12)
            budget_rolling_mean = math_insurance.moving_average(Company_budget_lesion_, n=4, post_mode=True)

            # matplotlibgraph.simple_graph([Company_budget_lesion_, budget_rolling_mean, budget_les_pr], range(73))
            # matplotlibgraph.simple_graph([Company_budget_lesion_[60:72], budget_rolling_mean[60:72], budget_les_pr[60:72]], range(12))

            predictions_rolling_mean = math_insurance.moving_average(budget_les_pr[(60-3):72], n=4)

            print('Оценка по сумме:')
            print(sum(budget_rolling_mean[60:72] - budget_les_pr[60:72]))

            print('Погрешность расходов:')
            print(sum(np.cumsum(Company_budget_lesion_[60:72])))
            print(sum(np.cumsum(budget_les_pr[60:72])))
            print(sum(np.cumsum(Company_budget_lesion_[60:72])) - sum(np.cumsum(budget_les_pr[60:72])))

            matplotlibgraph.simple_graph([math_insurance.moving_average(Company_budget_lesion_[60:72], n=4, post_mode=True), budget_les_pr[60:72]], range(12))

            # matplotlibgraph.simple_graph([budget_rolling_mean[60:72], predictions_rolling_mean], range(12))
            # matplotlibgraph.simple_graph([budget_rolling_mean[60:72] - predictions_rolling_mean], range(12))

        def method_second():

            budget_lesion_ma = math_insurance.moving_average(Company_budget_lesion_[0:60], n=6, post_mode=True)
            budget_lesion_prediction = math_insurance.sarimax(budget_lesion_ma, period=12)

            print('Оценка(выплаты):')
            diff = sum(budget_lesion_prediction) - sum(Company_budget_lesion_[60:72])
            print(diff)
            print('Погрешность(выплаты):')
            print(abs(diff)/sum(Company_budget_lesion_[60:72]))

            matplotlibgraph.simple_graph([Company_budget_lesion_[6:60], budget_lesion_ma], range(60-6))
            matplotlibgraph.simple_graph([Company_budget_lesion_[60:72], budget_lesion_prediction], range(12))

            budget_income_ma = math_insurance.moving_average(Company_budget_income_[0:60], n=3, post_mode=True)
            budget_income_prediction = math_insurance.holt_winters(budget_income_ma, period=12)

            print('Оценка(премии):')
            diff = sum(budget_income_prediction) - sum(Company_budget_income_[60:72])
            print(diff)
            print('Погрешность(премии):')
            print(abs(diff) / sum(Company_budget_income_[60:72]))

            # budget_income_post_ma = math_method.moving_average(Company_budget_lesion_[56:72], n=4, post_mode=True)
            # matplotlibgraph.simple_graph([Company_budget_income_[3:60], budget_income_ma], range(57))
            # matplotlibgraph.simple_graph([budget_income_post_ma, budget_income_prediction, Company_budget_income_[60:72]], range(12))

        def method_third(kf=0.004254):

            budget_lesion_prediction = math_insurance.arima_model((math_insurance.middle_value(Company_budget_lesion_[0:60], 12)), period=1)*12
            # print(math_method.middle_value(Company_budget_lesion_[0:60], 12))
            # print(budget_lesion_prediction, budget_lesion_prediction/12)
            diff = sum(budget_lesion_prediction) - sum(Company_budget_lesion_[60:72])
            print('Погрешность(выплаты):')
            print(abs(diff) / sum(Company_budget_lesion_[60:72]))
            print('После')
            print(sum(math_insurance.middle_value(Company_budget_lesion_[60:72], 12))*12)
            # budget_lesion_prediction

            sum_contracts_prediction = math_insurance.arima_model(Sum_contracts_[0:60], 12)
            diff = sum(sum_contracts_prediction) - sum(Sum_contracts_[60:72])
            print('Погрешность(суммы)')
            print(abs(diff) / sum(Sum_contracts_[60:72]))

            res_budget = [Company_budget_[60]]
            for iter in range(12):
                res_budget.append(0)
                diff_budget_income = sum_contracts_prediction[iter]*kf/12
                res_budget[iter+1] = res_budget[iter] + diff_budget_income - budget_lesion_prediction/12
            print("Предполагаемый капитал")
            print(res_budget[-1])
            print("Реальный капитал")
            print(Company_budget_[72])

            print("Погрешность капитала")
            diff = sum(res_budget[-1]) - Company_budget_[-1]
            pogr = abs(diff)/Company_budget_[-1]
            print(str(round(pogr*100, 2)), "%")



            print()
            print("Капитал на начало года", str(Company_budget_[60]))
            print("Предполагаемый капитал на конец года", str(sum(res_budget[-1])))

            clear_income = 5000000

            kf_new = kf/((clear_income + sum(budget_lesion_prediction))/sum(sum_contracts_prediction))
            kf_new = ((clear_income + sum(budget_lesion_prediction))/sum(sum_contracts_prediction))*12
            print()
            print("Ожидаемая чистая прибыль", str(clear_income))
            print("Рекомендуемая базовая ставка")
            print(kf_new)
            print("Или рекомендуемый параметр для расчета премии")
            print(kf_new/kf)

            # rt2 = Company_budget_lesion_[0:60]
            # rt = Sum_contracts_[0:60]
            # print()
            # print()
            # print(rt2)
            # print(budget_lesion_prediction)
            # print(rt)
            # print()
            # print()
            # print()















            # budget_lesion_ma = math_method.moving_average(Company_budget_lesion_[0:60], n=6, post_mode=True)
            # budget_lesion_prediction = math_method.sarimax(budget_lesion_ma, period=12)
            #
            # print('Оценка(выплаты):')
            # diff = sum(budget_lesion_prediction) - sum(Company_budget_lesion_[60:72])
            # print(diff)
            # print('Погрешность(выплаты):')
            # print(abs(diff)/sum(Company_budget_lesion_[60:72]))
            #
            # matplotlibgraph.simple_graph([Company_budget_lesion_[6:60], budget_lesion_ma], range(60-6))
            # matplotlibgraph.simple_graph([Company_budget_lesion_[60:72], budget_lesion_prediction], range(12))
            # #
            # budget_income_ma = math_method.moving_average(Company_budget_income_[0:60], n=3, post_mode=True)
            # budget_income_prediction = math_method.holt_winters(budget_income_ma, period=12)
            #
            # print('Оценка(премии):')
            # diff = sum(budget_income_prediction) - sum(Company_budget_income_[60:72])
            # # print(diff)
            # print('Погрешность(премии):')
            # print(abs(diff) / sum(Company_budget_income_[60:72]))
            #
            # budget_income_post_ma = math_method.moving_average(Company_budget_lesion_[56:72], n=4, post_mode=True)
            # matplotlibgraph.simple_graph([Company_budget_income_[3:60], budget_income_ma], range(57))
            # matplotlibgraph.simple_graph([budget_income_post_ma, budget_income_prediction, Company_budget_income_[60:72]], range(12))
            #
            # budget_les_pr = [0]*61 + math_method.holt_winters(
            #     math_method.moving_average(Company_budget_lesion_[0:60], n=4, post_mode=True), 12)
            # budget_rolling_mean = math_method.moving_average(Company_budget_lesion_, n=4, post_mode=True)
            # budget_rolling_mean = np.concatenate((budget_rolling_mean, [0]*4))
            # print(len(Company_budget_lesion_), len(budget_rolling_mean), len(budget_les_pr))
            # matplotlibgraph.simple_graph([Company_budget_lesion_, budget_rolling_mean, budget_les_pr], range(73))

        method_third()

    insurance_method(period * 12)