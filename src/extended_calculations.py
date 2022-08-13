
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

    for _ in range(months):
        not_depreciated *= one_plus_monthly_increase
        depreciated *= one_plus_monthly_increase
        depreciated *= one_minus_monthly_depreciation

    return not_depreciated + depreciated


def calculate_saving_with_detailed_allowance(base_value, list_of_allowances, monthly_rate_fraction, months):
    rate = 1.0 + monthly_rate_fraction
    value = base_value
    for month in range(months):
        value *= rate
        value += list_of_allowances[month]
    return value


def create_list_of_rent_payments(initial_value, annual_increase_fraction, months):
    list_of_payments = list()
    one_plus_increase = 1.0 + annual_increase_fraction
    value = initial_value
    for month in range(months):
        if month > 0 and (month % 12) == 0:
            value *= one_plus_increase
        list_of_payments.append(value)
    return list_of_payments


def create_lists_of_savings(mortgage_payment, list_of_rent_payments):
    first_month_rent_no_saving = None
    first_month_buy_saving = None
    saving_if_buy = list()
    saving_if_rent = list()
    for month, rent_payment in enumerate(list_of_rent_payments):
        if first_month_rent_no_saving is None and rent_payment >= mortgage_payment:
            first_month_rent_no_saving = month
        if first_month_buy_saving is None and mortgage_payment < rent_payment:
            first_month_buy_saving = month
        if mortgage_payment > rent_payment:
            saving_if_buy.append(0.0)
            saving_if_rent.append(mortgage_payment - rent_payment)
        elif mortgage_payment < rent_payment:
            saving_if_buy.append(rent_payment - mortgage_payment)
            saving_if_rent.append(0.0)
        else:
            saving_if_buy.append(0.0)
            saving_if_rent.append(0.0)

    return first_month_rent_no_saving, first_month_buy_saving, saving_if_buy, saving_if_rent


