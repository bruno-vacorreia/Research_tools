"""
Module containing functions for units conversion.
"""
from numpy import log10, ndarray, dtype, seterr
from scipy.constants import nu2lambda, lambda2nu

from research_tools.utils import Union, List, Any

DEFAULT_BAUD_RATE = 12.5e9
seterr(divide='ignore')


def lin2dB(value_lin: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert linear value to decibels (dB).

    :param value_lin: Linear value
    :return: Value in dB
    """
    return 10 * log10(value_lin)


def lin2dBm(value_lin: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert linear value to decibel-milliwatts (dBm).

    :param value_lin: Linear value
    :return: Value in dBm
    """
    return lin2dB(value_lin) + 30


def dB2lin(value_dB: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert decibels (dB) to linear value.

    :param value_dB: Value in dB
    :return: Linear value
    """
    return 10 ** (value_dB / 10)


def dBm2lin(value_dBm: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert decibel-milliwatts (dBm) to linear value.

    :param value_dBm: Value in dBm
    :return: Linear value
    """
    return dB2lin(value_dBm) * 1e-3


def wavelength2frequency(wavelength: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert wavelength to frequency.

    :param wavelength: Wavelength in meters
    :return: Frequency in Hz
    """
    return lambda2nu(wavelength)


def frequency2wavelength(freq: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert frequency to wavelength.

    :param freq: Frequency in Hz
    :return: Wavelength in meters
    """
    return nu2lambda(freq)


def delta_frequency2delta_wavelength(delta_f: float, frequency: float) -> float:
    """
    Convert change in frequency to change in wavelength.

    :param delta_f: Change in frequency in Hz
    :param frequency: Frequency in Hz
    :return: Change in wavelength in meters
    """
    wavelength = frequency2wavelength(frequency)
    return delta_f * wavelength / frequency


def delta_wavelength2delta_frequency(delta_wl: float, wavelength: float) -> float:
    """
    Convert change in wavelength to change in frequency.

    :param delta_wl: Change in wavelength in meters
    :param wavelength: Wavelength in meters
    :return: Change in frequency in Hz
    """
    frequency = wavelength2frequency(wavelength)
    return delta_wl * frequency / wavelength


def convert_snr(snr_dB: Union[float, List[float], ndarray[float], ndarray[Any, dtype]],
                actual_baud_rate: Union[float, List[float], ndarray[float], ndarray[Any, dtype]],
                new_baud_rate: Union[float, List[float], ndarray[float], ndarray[Any, dtype]] =
                DEFAULT_BAUD_RATE) -> Union[float, ndarray]:
    """
    Convert SNR from one baud rate to another.

    :param snr_dB: SNR in dB
    :param actual_baud_rate: Actual baud rate
    :param new_baud_rate: New baud rate (default is 12.5 GHz)
    :return: Converted SNR in dB
    """
    return snr_dB - lin2dB(new_baud_rate / actual_baud_rate)
