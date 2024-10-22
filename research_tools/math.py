"""
Module containing functions for mathematical operations.
"""
from numpy import seterr, array, sum

from research_tools.conversions import lin2dB, dB2lin

seterr(divide='ignore')


def snr_dB_sum(*args):
    """
    Calculate the sum of Signal-to-Noise Ratios (SNR) given in decibels (dB).

    :param args: Variable length argument list of SNR values in dB.
    :return: The combined SNR in dB.
    """
    snr_list = sum(1 / dB2lin(array(args)))

    return lin2dB(1 / snr_list)


if __name__ == '__main__':
    test_list = [41.76, 42.9, 40.06]
    test_array = array(test_list)

    print(round(snr_dB_sum(test_list), 2))
    print(round(snr_dB_sum(test_array), 2))
