import re


def country_code_format(country_code):
    """
    CHECK THE COUNTRY CODE FORMAT
    """
    if (not re.match('^[a-zA-Z]{2}$', country_code)):
        return False

    return True
