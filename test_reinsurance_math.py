from math_method import example
from math_method import matplotlibgraph
from math_method import math_insurance
from math_method.company_model import TypeInsurance, Contract, SimulatorInsurance
from math_method.example import OSAGO, KASKO
from reinsurance_math import math_reinsurance
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

    PERIOD_WORK_MONTH = 150
    PERIOD_PREDICTION_MONTH = 20

    SMOOTH_INTER = 3
    KF = 0.004254

    sim = SimulatorInsurance(time_mode=True)
    create_contracts_uni(sim, OSAGO, month=PERIOD_WORK_MONTH + PERIOD_PREDICTION_MONTH)
    Company_budget_income_, Company_budget_lesion_, Company_budget_, Sum_contracts_ = sim.simulator_period_trend(to_=PERIOD_WORK_MONTH + PERIOD_PREDICTION_MONTH, trend=example.example_trend_4)
    Company_budget_lesion_ = [x * (-1) for x in Company_budget_lesion_]

    capital_lesion = Company_budget_lesion_[0:PERIOD_WORK_MONTH]
    sum_contracts = Sum_contracts_[0:PERIOD_WORK_MONTH]
    last_capital = Company_budget_[PERIOD_WORK_MONTH]

    capital_prediction = math_reinsurance.forecasting(capital_lesion, sum_contracts, last_capital, PERIOD_PREDICTION_MONTH, SMOOTH_INTER, KF)

    print(f"Стартовый капитал {last_capital}")
    print(f"Предполагаемый капитал {capital_prediction[-1]}")
    print(f"Реальный капитал {Company_budget_[-1]}")



    # print(f"Настоящий бюджет {Company_budget_[PERIOD_WORK_MONTH]}")
    # print(f"Предполагаемый бюджет {res_budget[-1]}")
    # print(f"Конечный бюджет {Company_budget_[-1]}")
    # print(f"Погрешность {Company_budget_[-1] - res_budget[-1]}")
    # print(f"Погрешность % {((Company_budget_[-1] - res_budget[-1]) / abs(Company_budget_[PERIOD_WORK_MONTH] - Company_budget_[-1])) * 100}")
    #
    # matplotlibgraph.simple_graph([Company_budget_lesion_[0:PERIOD_WORK_MONTH], smooth_budget_lesion])
    # matplotlibgraph.simple_graph([Sum_contracts_[0:PERIOD_WORK_MONTH], smooth_sum_contracts])
    #
    # matplotlibgraph.simple_graph([Company_budget_, [i*0.99 for i in Company_budget_[0:PERIOD_WORK_MONTH]] + res_budget])