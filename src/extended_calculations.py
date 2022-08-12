
import sys

def convert_annual_nominal_interest_rate_to_monthly_effective(rate_fraction):
    return (1.0 + rate_fraction) ** (1.0 / 12.0) - 1.0


def increase_and_depreciation_calculation(asset_total_value,
                                          asset_depreciated_value,
                                          monthly_increase,
                                          monthly_depreciation,
                                          months
                                          ):
    not_depreciated = asset_total_value - asset_depreciated_value
    depreciated = asset_depreciated_value

    one_plus_monthly_increase = 1.0 + monthly_increase
    one_minus_monthly_depreciation = 1.0 - monthly_depreciation

    print('-----')
    for _ in range(months):
        not_depreciated *= one_plus_monthly_increase
        depreciated *= one_plus_monthly_increase
        depreciated *= one_minus_monthly_depreciation
        print(not_depreciated, '\t', depreciated)

    print('-----')
    print()
    sys.stdout.flush()

    return not_depreciated + depreciated


def calculate_saving_with_detailed_allowance(base_value, list_of_allowances, monthly_rate_fraction, months):
    rate = 1.0 + monthly_rate_fraction
    value = base_value
    for month in range(months):
        value *= rate
        value += list_of_allowances[month]
    return value


def create_list_of_rate_payments(initial_value, annual_increase_fraction, months):
    list_of_payments = list()
    one_plus_increase = 1.0 + annual_increase_fraction
    value = initial_value
    for month in months:
        if month > 0 and (months % 12) == 0:
            value *= one_plus_increase
        list_of_payments.append(value)
    return list_of_payments
