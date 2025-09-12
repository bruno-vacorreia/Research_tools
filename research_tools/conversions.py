"""
Module containing functions for units conversion.
"""
from numpy import log10, ndarray, dtype, seterr, array
from scipy.constants import nu2lambda, lambda2nu

from research_tools.utils import Union, List, Any, Tuple

DEFAULT_BAUD_RATE = 12.5e9
seterr(divide='ignore')


def lin2dB(value_lin: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert linear value to decibels (dB).

    :param value_lin: Linear value
    :return: Value in dB
    """
    flag_list = False
    if isinstance(value_lin, list):
        value_lin = array(value_lin)
        flag_list = True

    if flag_list:
        return list(10 * log10(value_lin))
    else:
        return 10 * log10(value_lin)


def lin2dBm(value_lin: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert linear value to decibel-milliwatts (dBm).

    :param value_lin: Linear value
    :return: Value in dBm
    """
    flag_list = False
    if isinstance(value_lin, list):
        value_lin = array(value_lin)
        flag_list = True

    if flag_list:
        return list(lin2dB(value_lin) + 30)
    else:
        return lin2dB(value_lin) + 30


def dB2lin(value_dB: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert decibels (dB) to linear value.

    :param value_dB: Value in dB
    :return: Linear value
    """
    flag_list = False
    if isinstance(value_dB, list):
        value_dB = array(value_dB)
        flag_list = True

    if flag_list:
        return list(10 ** (value_dB / 10))
    else:
        return 10 ** (value_dB / 10)


def dBm2lin(value_dBm: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert decibel-milliwatts (dBm) to linear value.

    :param value_dBm: Value in dBm
    :return: Linear value
    """
    flag_list = False
    if isinstance(value_dBm, list):
        value_dBm = array(value_dBm)
        flag_list = True

    if flag_list:
        return list(dB2lin(value_dBm) * 1e-3)
    else:
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


def convert_snr(snr_dB: Union[float, List[float], ndarray[Any, dtype]],
                actual_baud_rate: Union[float, List[float], ndarray[Any, dtype]],
                new_baud_rate: Union[float, List[float], ndarray[Any, dtype]] =
                DEFAULT_BAUD_RATE) -> Union[float, ndarray]:
    """
    Convert SNR from one baud rate to another.

    :param snr_dB: SNR in dB
    :param actual_baud_rate: Actual baud rate
    :param new_baud_rate: New baud rate (default is 12.5 GHz)
    :return: Converted SNR in dB
    """
    flag_list = False
    if isinstance(actual_baud_rate, list):
        actual_baud_rate = array(actual_baud_rate)
    if isinstance(new_baud_rate, list):
        new_baud_rate = array(new_baud_rate)
    if isinstance(snr_dB, list):
        snr_dB = array(snr_dB)
        flag_list = True

    new_snr_dB = snr_dB - lin2dB(new_baud_rate / actual_baud_rate)

    if flag_list:
        new_snr_dB = list(new_snr_dB)

    return new_snr_dB


def binary_to_hex(binary_str: str) -> str:
    """
    Convert binary string to hexadecimal string.

    :param binary_str: Binary string
    :return: Hexadecimal string
    """
    # Convert binary string to an integer
    decimal = int(binary_str, 2)
    # Convert integer to hexadecimal string
    hex_str = hex(decimal)

    # Remove the '0x' prefix
    return hex_str[2:]


def hex_to_binary(hex_str: str) -> str:
    """
    Convert hexadecimal string to binary string.

    :param hex_str: Hexadecimal string
    :return: Binary string
    """
    # Convert hexadecimal string to an integer
    decimal = int(hex_str, 16)
    # Convert integer to binary string
    binary_str = bin(decimal)

    # Remove the '0b' prefix
    return binary_str[2:]


def decimal_to_dms(decimal_degree: float) -> Tuple[int, int, int]:
    """
    Convert position in decimal degree format to degree, minute and second format.

    :param decimal_degree: Position in decimal degree
    :return: Position in degree, minute and second format
    """
    sing = 1 if decimal_degree > 0 else -1
    degrees = int(decimal_degree)
    minutes_float = abs(decimal_degree - degrees) * 60
    minutes = int(minutes_float)
    seconds = round(abs(minutes_float - minutes) * 60)

    return degrees, sing * minutes, sing * seconds


def dms_to_decimal(degrees: int, minutes: int, seconds: int) -> float:
    """
    Convert position in degree, minute and second format to decimal degree format.

    :param degrees: Position degree
    :param minutes: Position minute
    :param seconds: Position second
    :return: Position in decimal degree
    """
    sign = -1 if any(value < 0 for value in [degrees, minutes, seconds]) else 1

    return sign * (abs(degrees) + abs(minutes) / 60 + abs(seconds) / 3600)
