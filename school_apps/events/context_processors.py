from nepalicalendar.nepcal import NepDate, NepCal, values


def to_nepali(number):
    return number


def inject_date_params(request):
    """
    Injects a 'today' variable in template context
    """
    return {
        "today": NepDate.today(),
        "nepcal_values": values,
        "nepali_days_range": range(1, 33),
        "nepali_years": range(values.START_NP_YEAR, values.END_NP_YEAR + 1),
    }
