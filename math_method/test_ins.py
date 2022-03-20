import example
import matplotlibgraph
import math_insurance
from company_model import TypeInsurance, Contract, SimulatorInsurance
from example import OSAGO, KASKO
import random

# PERIOD_WORK = 5
# PERIOD_PREDICTION = 2


def create_contracts_uni(object_SimulatorInsurance, object_TypeInsurance, month=24):
    object_SimulatorInsurance.list_TypeInsurance.append(object_TypeInsurance)
    object_SimulatorInsurance.create_contracts(object_TypeInsurance=object_SimulatorInsurance.list_TypeInsurance[0],
                                               num_contracts=random.randint(int(1000 * month / 12), int(5000 * month / 12)),
                                               timestamp_from_from_=-1 * month,
                                               timestamp_from_to_=2 * month)


if __name__ == '__main__':

    # PERIOD_WORK_MONTH = PERIOD_WORK * 12
    # PERIOD_PREDICTION_MONTH = PERIOD_PREDICTION * 12

    PERIOD_WORK_MONTH = 150
    PERIOD_PREDICTION_MONTH = 100

    SMOOTH_INTER = 3
    kf = 0.004254

    sim = SimulatorInsurance(time_mode=True)
    create_contracts_uni(sim, OSAGO, month=PERIOD_WORK_MONTH + PERIOD_PREDICTION_MONTH)
    Company_budget_income_, Company_budget_lesion_, Company_budget_, Sum_contracts_ = sim.simulator_period_trend(to_=PERIOD_WORK_MONTH + PERIOD_PREDICTION_MONTH, trend=example.example_trend_5)
    Company_budget_lesion_ = [x * (-1) for x in Company_budget_lesion_]

    # if False:
    #
    #     print(Company_budget_income_)
    #     print(Company_budget_lesion_)
    #     print(Company_budget_)
    #     print(Sum_contracts_)
    #
    #     print('==1==')
    #
    #     smooth_budget_lesion = math_insurance.middle_value(Company_budget_lesion_[0:60], 12)
    #     budget_lesion_prediction = math_insurance.arima_model(smooth_budget_lesion, 1)
    #
    #     sum_contracts_prediction = math_insurance.arima_model(Sum_contracts_[0:60], 12)
    #
    #     res_budget = [Company_budget_[60]]
    #     for iter in range(12):
    #         res_budget.append(0)
    #         diff_budget_income = sum_contracts_prediction[iter] * kf / 12
    #         res_budget[iter + 1] = res_budget[iter] + diff_budget_income - budget_lesion_prediction
    #
    #     print(f"Начальный бюджет {Company_budget_[0]}")
    #     print(f"Предполагаемый бюджет {res_budget[-1]}")
    #     print(f"Конечный бюджет {Company_budget_[-1]}")
    #     print(f"Погрешность {Company_budget_[-1] - res_budget[-1]}")
    #     print(f"Погрешность % {((Company_budget_[-1] - res_budget[-1]) / ((res_budget[-1] + Company_budget_[0]) / 2)) * 100}")
    #
    #     print('==2==')
    #
    #     smooth_budget_lesion = math_insurance.smoothing_middle(Company_budget_lesion_[0:60], 4)
    #     budget_lesion_prediction = math_insurance.arima_model(smooth_budget_lesion, 12)
    #
    #     smooth_sum_contracts = math_insurance.smoothing_middle(Sum_contracts_[0:60], 4)
    #     sum_contracts_prediction = math_insurance.arima_model(smooth_sum_contracts, 12)
    #
    #     # print(smooth_budget_lesion)
    #     # print(budget_lesion_prediction)
    #     # print(sum_contracts_prediction)
    #     # print(res_budget)
    #
    #     res_budget = [Company_budget_[60]]
    #     for iter in range(12):
    #         diff_budget_income = sum_contracts_prediction[iter] * kf / 12
    #         res_budget.append(res_budget[iter] + diff_budget_income - budget_lesion_prediction[iter])
    #
    #     print(f"Начальный бюджет {Company_budget_[0]}")
    #     print(f"Предполагаемый бюджет {res_budget[-1]}")
    #     print(f"Конечный бюджет {Company_budget_[-1]}")
    #     print(f"Погрешность {Company_budget_[-1] - res_budget[-1]}")
    #     print(f"Погрешность % {((Company_budget_[-1] - res_budget[-1]) / ((res_budget[-1] + Company_budget_[0]) / 2)) * 100}")
    #
    #     matplotlibgraph.simple_graph([Company_budget_lesion_[0:60], smooth_budget_lesion])
    #     matplotlibgraph.simple_graph([Sum_contracts_[0:60], smooth_sum_contracts])

    smooth_budget_lesion = math_insurance.smoothing_middle(Company_budget_lesion_[0:PERIOD_WORK_MONTH], SMOOTH_INTER)
    budget_lesion_prediction = math_insurance.arima_model(smooth_budget_lesion, PERIOD_PREDICTION_MONTH)

    smooth_sum_contracts = math_insurance.smoothing_middle(Sum_contracts_[0:PERIOD_WORK_MONTH], SMOOTH_INTER)
    sum_contracts_prediction = math_insurance.arima_model(smooth_sum_contracts, PERIOD_PREDICTION_MONTH)

    res_budget = [Company_budget_[PERIOD_WORK_MONTH]]
    for iter in range(PERIOD_PREDICTION_MONTH):
        diff_budget_income = sum_contracts_prediction[iter] * kf / 12
        res_budget.append(res_budget[iter] + diff_budget_income - budget_lesion_prediction[iter])

    # print(f"Стартовый бюджет {Company_budget_[0]}")
    print(f"Настоящий бюджет {Company_budget_[PERIOD_WORK_MONTH]}")
    print(f"Предполагаемый бюджет {res_budget[-1]}")
    print(f"Конечный бюджет {Company_budget_[-1]}")
    print(f"Погрешность {Company_budget_[-1] - res_budget[-1]}")
    print(f"Погрешность % {((Company_budget_[-1] - res_budget[-1]) / abs(Company_budget_[PERIOD_WORK_MONTH] - Company_budget_[-1])) * 100}")

    # matplotlibgraph.simple_graph([Company_budget_lesion_[0:PERIOD_WORK * 12], smooth_budget_lesion])
    matplotlibgraph.simple_graph([Sum_contracts_[0:PERIOD_WORK_MONTH], smooth_sum_contracts])

    matplotlibgraph.simple_graph([Company_budget_, [i*0.95 for i in Company_budget_[0:PERIOD_WORK_MONTH]] + res_budget])
