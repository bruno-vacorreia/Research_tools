"""
Module containing functions for units conversion.
"""
from numpy import log10, ndarray, dtype, seterr
from scipy.constants import nu2lambda, lambda2nu

from personal_tools.utils import Union, List, Any

DEFAULT_BAUD_RATE = 12.5e9
seterr(divide='ignore')


def lin2dB(value_lin):
    return 10 * log10(value_lin)


def lin2dBm(value_lin):
    return lin2dB(value_lin) + 30


def dB2lin(value_dB):
    return 10 ** (value_dB / 10)


def dBm2lin(value_dBm):
    return dB2lin(value_dBm) * 1e-3


def wavelength2frequency(wavelength):
    return lambda2nu(wavelength)


def frequency2wavelength(freq):
    return nu2lambda(freq)


def delta_frequency2delta_wavelength(delta_f, frequency):
    wavelength = frequency2wavelength(frequency)
    return delta_f * wavelength / frequency


def delta_wavelength2delta_frequency(delta_wl, wavelength):
    frequency = wavelength2frequency(wavelength)
    return delta_wl * frequency / wavelength


def convert_snr(snr_dB: Union[float, List[float], ndarray[float], ndarray[Any, dtype]],
                actual_baud_rate: Union[float, List[float], ndarray[float], ndarray[Any, dtype]],
                new_baud_rate: Union[float, List[float], ndarray[float], ndarray[Any, dtype]] = DEFAULT_BAUD_RATE):

    return snr_dB - lin2dB(new_baud_rate / actual_baud_rate)
