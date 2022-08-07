
def calc_annual_to_monthly_rate_for_saving(annual_rate_percent: float) -> float:
    annual_yield = 1.0 + (annual_rate_percent / 100.0)
    return annual_yield ** (1.0 / 12.0) - 1.0


def calc_saving(initial, monthly, months, annual_rate_percent):
    rate = calc_annual_to_monthly_rate_for_saving(annual_rate_percent)
    # rate = (annual_rate_percent/100.0)/12.0
    total = initial
    for _ in range(int(months)):
        total = total * (1.0 + rate)
        total = total + monthly
    return total


def calculate_spitzer(loan, mortgage_rate_percent, months):
    rate = (mortgage_rate_percent / 100.0) / 12.0
    mortgage_payment = rate * loan * (((1.0 + rate) ** months) / (((1.0 + rate) ** months) - 1.0))
    return mortgage_payment


class Calculate(object):
    def __init__(self, apartment, immediate_payment, rent_monthly, years, mortgage_rate, saving_rate):
        self.apartment, self.immediate_payment, self.rent_monthly, self.years, self.mortgage_rate, self.saving_rate = apartment, immediate_payment, rent_monthly, years, mortgage_rate, saving_rate
        self.months = years * 12.0

        self.mortgage_payment = None
        self.total_cost_of_apartment = None
        self.total_saving_if_rent = None
        self.total_saving_if_buy = None
        self.total_if_buy = None
        self.monthly_saving = None
        self.rent_smaller_than_mortgage = True

    def calculate(self):
        loan = self.apartment - self.immediate_payment
        self.mortgage_payment = calculate_spitzer(loan, self.mortgage_rate, self.months)
        self.total_cost_of_apartment = self.immediate_payment + self.mortgage_payment * self.months

        initial_saving = self.immediate_payment
        self.monthly_saving = self.mortgage_payment - self.rent_monthly

        if self.monthly_saving >= 0:
            self.rent_smaller_than_mortgage = True
            self.total_saving_if_rent = calc_saving(initial_saving, self.monthly_saving, self.months, self.saving_rate)
            self.total_if_buy = self.apartment
        else:
            self.rent_smaller_than_mortgage = False
            self.total_saving_if_rent = calc_saving(initial_saving, 0.0, self.months, self.saving_rate)
            self.total_saving_if_buy = calc_saving(0.0, -self.monthly_saving, self.months, self.saving_rate)
            self.total_if_buy = self.apartment + self.total_saving_if_buy


