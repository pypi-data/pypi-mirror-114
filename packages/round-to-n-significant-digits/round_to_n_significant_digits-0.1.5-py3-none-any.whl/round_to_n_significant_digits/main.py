"""Main module with main function rtnsd"""
# Standard library imports
from math import floor
from math import log10

# Third party imports

# Local imports

def rtnsd(float_num, int_digits=1):
    """[summary]

    Args:
        float_num (float): float number to round
        int_digits (int): How many significant digits you need. Defaults to 1.
    """
    if not isinstance(float_num, (float, int)):
        raise TypeError("Unable to round number with type %s " % (
            str(type(float_num))
        ))


    if not float_num:
        return 0.0
    int_sign_digits = floor(log10(abs(float_num)))
    return round(float_num, int_digits - int(int_sign_digits) - 1)
