
from extended_calculations import \
    convert_annual_nominal_interest_rate_to_monthly_effective, \
    increase_and_depreciation_calculation, \
    create_list_of_rent_payments, create_lists_of_savings, calculate_saving_with_detailed_allowance




def calc_saving(initial, monthly, months, annual_rate_percent):
    rate = convert_annual_nominal_interest_rate_to_monthly_effective(annual_rate_percent / 100.0)
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
    def __init__(self, apartment, immediate_payment, rent_monthly, years, mortgage_rate, saving_rate,
                 annual_increase_apartment_percent, building_worth, annual_depreciation_percent,
                 annual_increase_rent_percent
                 ):
        self.apartment, self.immediate_payment, self.rent_monthly, self.years, self.mortgage_rate, self.saving_rate = apartment, immediate_payment, rent_monthly, years, mortgage_rate, saving_rate
        self.annual_increase_apartment_percent, self.building_worth, self.annual_depreciation_percent = annual_increase_apartment_percent, building_worth, annual_depreciation_percent
        self.annual_increase_rent_percent = annual_increase_rent_percent
        self.months = years * 12.0

        self.mortgage_payment = None
        self.total_cost_of_apartment = None
        self.total_saving_if_rent = None
        self.total_saving_if_buy = None
        self.apartment_value_at_end = None
        self.total_if_buy = None
        self.first_month_rent_no_saving, self.first_month_buy_saving, self.saving_list_if_buy, self.saving_list_if_rent = None, None, None, None

    def calculate(self):
        loan = self.apartment - self.immediate_payment
        self.mortgage_payment = calculate_spitzer(loan, self.mortgage_rate, self.months)
        self.total_cost_of_apartment = self.immediate_payment + self.mortgage_payment * self.months
        self.apartment_value_at_end = self._calculate_apartment_value_at_end()

        list_of_rent_payments = create_list_of_rent_payments(self.rent_monthly, self.annual_increase_rent_percent / 100.0, int(self.months))
        self.first_month_rent_no_saving, self.first_month_buy_saving, self.saving_list_if_buy, self.saving_list_if_rent = create_lists_of_savings(self.mortgage_payment, list_of_rent_payments)
        saving_monthly_effective_rate = convert_annual_nominal_interest_rate_to_monthly_effective(self.saving_rate / 100.0)
        self.total_saving_if_rent = calculate_saving_with_detailed_allowance(self.immediate_payment, self.saving_list_if_rent, saving_monthly_effective_rate, int(self.months))
        self.total_saving_if_buy = calculate_saving_with_detailed_allowance(0.0, self.saving_list_if_buy, saving_monthly_effective_rate, int(self.months))
        self.total_if_buy = self.apartment_value_at_end + self.total_saving_if_buy





        #
        #
        #
        #
        # self.monthly_saving = self.mortgage_payment - self.rent_monthly
        #
        # if self.monthly_saving >= 0:
        #     self.rent_smaller_than_mortgage = True
        #     self.total_saving_if_rent = calc_saving(initial_saving, self.monthly_saving, self.months, self.saving_rate)
        #     self.total_if_buy = self.apartment_value_at_end
        # else:
        #     self.rent_smaller_than_mortgage = False
        #     self.total_saving_if_rent = calc_saving(initial_saving, 0.0, self.months, self.saving_rate)
        #     self.total_saving_if_buy = calc_saving(0.0, -self.monthly_saving, self.months, self.saving_rate)
        #     self.total_if_buy = self.apartment_value_at_end + self.total_saving_if_buy

    def _calculate_apartment_value_at_end(self):
        # self.annual_increase_apartment_percent, self.building_worth, self.annual_depreciation_percent
        monthly_increase = convert_annual_nominal_interest_rate_to_monthly_effective(self.annual_increase_apartment_percent / 100.0)
        monthly_depreciation = -convert_annual_nominal_interest_rate_to_monthly_effective(- self.annual_depreciation_percent / 100.0)
        return increase_and_depreciation_calculation(self.apartment, self.building_worth, monthly_increase, monthly_depreciation, int(self.months))




