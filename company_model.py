from dataclasses import dataclass
import functools
import random


@dataclass
class TypeInsurance:
    id_type: int
    name: str
    base_rate: float
    parameters_ins: list[float]
    month_mode: bool = False

    def __post_init__(self):
        self.price_ins = self.base_rate * functools.reduce(lambda a, b: a * b, self.parameters_ins)
        if self.month_mode: self.price_ins = self.price_ins / 12


@dataclass
class Contract:
    id_contract: int
    name: str
    sum: float
    timestamp_from_: int
    timestamp_to_: int
    type_insurance: TypeInsurance
    parameters: list[float]

    def __post_init__(self):
        self.price = self.sum * self.type_insurance.price_ins * functools.reduce(lambda a, b: a * b, self.parameters)


@dataclass
class Payout:
    id_payout: int
    contract: Contract
    timestamp: int

    def __post_init__(self):
        self.sum = self.contract.sum


class SimulatorInsurance:

    list_TypeInsurance = []
    list_Contracts = []
    list_Payout = []

    def __init__(self,
                 time_mode=False,
                 ):

        self.time_mode = time_mode

    def create_payout(self,
                      contract: Contract,
                      timestamp: int,
                      id_payout: int = 12345678):

        self.list_Payout.append(Payout(id_payout=id_payout,
                                       contract=contract,
                                       timestamp=timestamp))

    def create_contracts(self,
                         object_TypeInsurance: TypeInsurance,
                         num_contracts: int = 100,
                         sum_from_: int = 100000,
                         sum_to_: int = 1550000,
                         timestamp_from_from_=-12,
                         timestamp_from_to_=24,
                         timestamp_duration_from_=1,
                         timestamp_duration_to_=48):

        for i in range(num_contracts):
            timestamp_from_ = random.randint(timestamp_from_from_, timestamp_from_to_)
            timestamp_to_ = timestamp_from_ + random.randint(timestamp_duration_from_, timestamp_duration_to_)
            new_contracts = Contract(id_contract=12345,
                                     name='simple_contract',
                                     sum=random.randint(sum_from_, sum_to_),
                                     timestamp_from_=timestamp_from_,
                                     timestamp_to_=timestamp_to_,
                                     type_insurance=object_TypeInsurance,
                                     parameters=[1])
            self.list_Contracts.append(new_contracts)

    def simulator_period_random(self,
                                to_,
                                capital=10000000,
                                type_insurance:
                                TypeInsurance = None):

        Company_budget = []
        Company_budget_diff = []

        Company_budget_diff.append(0)
        Company_budget.append(capital)

        for iter in range(to_):
            for object_Contract in self.list_Contracts:
                if object_Contract.timestamp_from_ - 1 < iter < object_Contract.timestamp_to_ + 1 \
                        and (type_insurance == object_Contract.type_insurance or not type_insurance):
                    Company_budget_diff[iter] = Company_budget_diff[iter] + object_Contract.price

                    bool_ = random.choices([True, False], weights=[random.uniform(0, 25)/12, 7073])[0]

                    if bool_:
                        Company_budget_diff[iter] = Company_budget_diff[iter] - object_Contract.sum
                        object_Contract.timestamp_to_ = iter

                        new_Contract = Contract(id_contract=object_Contract.id_contract,
                                                name=object_Contract.name,
                                                sum=object_Contract.sum,
                                                timestamp_from_=iter + 3,
                                                timestamp_to_=iter + 3 + random.randint(6, 12),
                                                type_insurance=object_Contract.type_insurance,
                                                parameters=[1.3])
                        self.list_Contracts.append(new_Contract)

            Company_budget[iter] = Company_budget[iter] + Company_budget_diff[iter]
            Company_budget.append(Company_budget[iter])
            Company_budget_diff.append(0)

        return Company_budget_diff, Company_budget

    def simulator_period_trend(self,
                               to_,
                               trend: list,
                               capital=10000000,
                               type_insurance: TypeInsurance = None):

        Company_budget = []
        Company_budget_income = []
        Company_budget_lesion = []
        Sum_contracts_ = []

        Company_budget_income.append(0)
        Company_budget_lesion.append(0)
        Company_budget.append(capital)
        Sum_contracts_.append(0)

        for iter in range(to_):
            for object_Contract in self.list_Contracts:
                if object_Contract.timestamp_from_ - 1 < iter < object_Contract.timestamp_to_ + 1 \
                        and (type_insurance == object_Contract.type_insurance or not type_insurance):
                    Company_budget_income[iter] = Company_budget_income[iter] + object_Contract.price
                    Sum_contracts_[iter] = Sum_contracts_[iter] + object_Contract.sum

                    bool_ = random.choices([True, False], weights=[trend[(iter % len(trend))]/10, 1])[0]
                    # if bool_: print(iter, len(trend), (iter % len(trend)), trend[(iter % len(trend))], bool_)

                    if bool_:
                        Company_budget_lesion[iter] = Company_budget_lesion[iter] - object_Contract.sum
                        object_Contract.timestamp_to_ = iter

                        new_Contract = Contract(id_contract=object_Contract.id_contract,
                                                name=object_Contract.name,
                                                sum=object_Contract.sum,
                                                timestamp_from_=iter + 3,
                                                timestamp_to_=iter + 3 + random.randint(6, 12),
                                                type_insurance=object_Contract.type_insurance,
                                                parameters=[1.3])
                        self.list_Contracts.append(new_Contract)

            Company_budget[iter] = Company_budget[iter] + Company_budget_income[iter] + Company_budget_lesion[iter]
            Company_budget.append(Company_budget[iter])

            Company_budget_income.append(0)
            Company_budget_lesion.append(0)
            Sum_contracts_.append(0)

        return Company_budget_income, Company_budget_lesion, Company_budget, Sum_contracts_

    def simulator_payout(self,
                         from_: int,
                         to_: int,
                         type_insurance: TypeInsurance,
                         trend: list = None,
                         update_contract: bool = False):

        for iter in range(from_, to_):
            for object_Contract in self.list_Contracts:
                if object_Contract.timestamp_from_ <= iter <= object_Contract.timestamp_to_ \
                        and (type_insurance == object_Contract.type_insurance or not type_insurance):

                    if trend: bool_ = random.choices([True, False], weights=[trend[(iter % len(trend))]/10, 1])[0]
                    else: bool_ = random.choices([True, False], weights=[random.uniform(0, 25)/12, 7073])[0]

                    if bool_:

                        object_Contract.timestamp_to_ = iter
                        self.create_payout(timestamp=iter, contract=object_Contract)

                        if update_contract:
                            new_Contract = Contract(id_contract=object_Contract.id_contract,
                                                    name=object_Contract.name,
                                                    sum=object_Contract.sum,
                                                    timestamp_from_=iter + 3,
                                                    timestamp_to_=iter + 3 + random.randint(6, 12),
                                                    type_insurance=object_Contract.type_insurance,
                                                    parameters=[1.3])
                            self.list_Contracts.append(new_Contract)


