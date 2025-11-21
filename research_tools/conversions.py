"""
Module containing functions for units conversion.
"""
from numpy import log10, ndarray, dtype, seterr, asanyarray, any as np_any
from typing import Union, List, Any, Tuple

from research_tools.constants import DEFAULT_BAUD_RATE, c

seterr(divide='ignore')


def lin2dB(value_lin: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert linear value to decibels (dB).
    Maintain the same input type.

    :param value_lin: Linear value
    :return: Value in dB
    """
    flag_convert = True if isinstance(value_lin, (float, list)) else False
    value_lin = asanyarray(value_lin)

    return (10 * log10(value_lin)).tolist()  if flag_convert else 10 * log10(value_lin)


def lin2dBm(value_lin: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert linear value to decibel-milliwatts (dBm).
    Maintain the same input type.

    :param value_lin: Linear value
    :return: Value in dBm
    """
    flag_convert = True if isinstance(value_lin, (float, list)) else False
    value_lin = asanyarray(value_lin)

    return (lin2dB(value_lin) + 30).tolist() if flag_convert else lin2dB(value_lin) + 30


def dB2lin(value_dB: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert decibels (dB) to linear value.

    :param value_dB: Value in dB
    :return: Linear value
    """
    flag_convert = True if isinstance(value_dB, (float, list)) else False
    value_dB = asanyarray(value_dB)

    return (10 ** (value_dB / 10)).tolist() if flag_convert else 10 ** (value_dB / 10)


def dBm2lin(value_dBm: Union[float, list, ndarray]) -> Union[float, list, ndarray]:
    """
    Convert decibel-milliwatts (dBm) to linear value.

    :param value_dBm: Value in dBm
    :return: Linear value
    """
    flag_convert = True if isinstance(value_dBm, (float, list)) else False
    value_dBm = asanyarray(value_dBm)

    return (dB2lin(value_dBm) * 1e-3).tolist() if flag_convert else dB2lin(value_dBm) * 1e-3


def wavelength2frequency(wavelength: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert wavelength to frequency.

    :param wavelength: Wavelength in meters
    :return: Frequency in Hz
    """
    if np_any(wavelength == 0.0):
        raise ZeroDivisionError('Wavelength cannot be zero')
    elif np_any(wavelength < 0.0):
        raise ValueError('Wavelength cannot be negative')

    return c / wavelength


def frequency2wavelength(freq: Union[float, ndarray]) -> Union[float, ndarray]:
    """
    Convert frequency to wavelength.

    :param freq: Frequency in Hz
    :return: Wavelength in meters
    """
    if np_any(freq == 0.0):
        raise ZeroDivisionError('Frequency cannot be zero')
    elif np_any(freq < 0.0):
        raise ValueError('Frequency cannot be negative')

    return c / freq


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
    flag_convert = True if isinstance(snr_dB, (float, list)) else False

    new_snr_dB = asanyarray(snr_dB) - lin2dB(asanyarray(new_baud_rate) / asanyarray(actual_baud_rate))
    return new_snr_dB.tolist() if flag_convert else new_snr_dB


def binary_to_hex(binary_str: str, same_length: bool = True) -> str:
    """
    Convert binary string to hexadecimal string.

    :param binary_str: Binary string
    :param same_length: Option to maintain the same number of digits. Default True
    :return: Hexadecimal string
    """
    # Convert binary string to an integer
    decimal = int(binary_str, 2)
    # Convert integer to hexadecimal string and remove the '0x' prefix
    hex_str = hex(decimal)[2:]
    hex_str = hex_str.zfill(len(binary_str) // 4) if same_length else hex_str

    return hex_str


def hex_to_binary(hex_str: str, same_length: bool = True) -> str:
    """
    Convert hexadecimal string to binary string.

    :param hex_str: Hexadecimal string
    :param same_length: Option to maintain the same number of digits. Default True
    :return: Binary string
    """
    # Convert hexadecimal string to an integer
    decimal = int(hex_str, 16)
    # Convert integer to binary string and Remove the '0b' prefix
    binary_str = bin(decimal)[2:]
    binary_str = binary_str.zfill(len(hex_str) * 4) if same_length else binary_str

    return binary_str


def decimal_to_dms(decimal_degree: float) -> Tuple[int, int, int]:
    """
    Convert position in decimal degree format to degree, minute and second format.

    :param decimal_degree: Position in decimal degree
    :return: Position in degree, minute and second format
    """
    sing = 1 if decimal_degree > 0.0 else -1
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
    if not all(isinstance(value, int) for value in [degrees, minutes, seconds]):
        raise TypeError('Argument must be int')
    sign = -1 if any(value < 0 for value in [degrees, minutes, seconds]) else 1

    return sign * (abs(degrees) + abs(minutes) / 60 + abs(seconds) / 3600)
