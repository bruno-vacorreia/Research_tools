import pytest
import numpy as np
from scipy.constants import c


from research_tools.conversions import (
    lin2dB, lin2dBm, dB2lin, dBm2lin,
    wavelength2frequency, frequency2wavelength,
    delta_frequency2delta_wavelength, delta_wavelength2delta_frequency,
    convert_snr, DEFAULT_BAUD_RATE,
    binary_to_hex, hex_to_binary,
    decimal_to_dms, dms_to_decimal
)

def lin2dB_lin2dBm(result, expected_special_value):
    if isinstance(result, list):
        assert len(result) == len(expected_special_value)
        for i in range(len(result)):
            if np.isinf(expected_special_value[i]):
                assert np.isinf(result[i]) and np.sign(result[i]) == np.sign(expected_special_value[i])
            elif np.isnan(expected_special_value[i]):
                assert np.isnan(result[i])
            else:
                assert result[i] == pytest.approx(expected_special_value[i])
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_special_value, equal_nan=True)
    else:
        if np.isinf(expected_special_value):
            assert np.isinf(result) and np.sign(result) == np.sign(expected_special_value)
        elif np.isnan(expected_special_value):
            assert np.isnan(result)
        else:
            assert result == pytest.approx(expected_special_value)

# --- Test lin2dB function ---
@pytest.mark.parametrize("value_lin, expected_dB", [
    (1.0, 0.0),
    (10.0, 10.0),
    (100.0, 20.0),
    (0.1, -10.0),
    (0.001, -30.0),
    (np.array([1.0, 10.0]), np.array([0.0, 10.0])),
    ([1.0, 10.0], [0.0, 10.0]),
])
def test_lin2dB_normal_cases(value_lin, expected_dB):
    """Tests lin2dB with normal float, numpy array, and list inputs."""
    result = lin2dB(value_lin)
    if isinstance(result, list):
        assert np.allclose(result, expected_dB)
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_dB)
    else:
        assert result == pytest.approx(expected_dB)

@pytest.mark.parametrize("value_lin, expected_special_value", [
    (0.0, -np.inf),  # log10(0) is -inf
    (-1.0, np.nan),  # log10(negative) is nan
    (np.array([0.0, -1.0]), np.array([-np.inf, np.nan])),
    ([0.0, -1.0], [-np.inf, np.nan]),
])
def test_lin2dB_edge_cases(value_lin, expected_special_value):
    """Tests lin2dB with edge cases like zero and negative inputs."""
    result = lin2dB(value_lin)
    lin2dB_lin2dBm(result, expected_special_value)


# noinspection PyTypeChecker
def test_lin2dB_error_handling():
    """Tests lin2dB with invalid input types."""
    with pytest.raises(TypeError):
        lin2dB("invalid")
    with pytest.raises(TypeError):
        lin2dB(None)

# --- Test lin2dBm function ---
@pytest.mark.parametrize("value_lin, expected_dBm", [
    (1.0, 30.0),
    (10.0, 40.0),
    (0.001, 0.0),
    (np.array([1.0, 0.001]), np.array([30.0, 0.0])),
    ([1.0, 0.001], [30.0, 0.0]),
])
def test_lin2dBm_normal_cases(value_lin, expected_dBm):
    """Tests lin2dBm with normal float, numpy array, and list inputs."""
    result = lin2dBm(value_lin)
    if isinstance(result, list):
        assert np.allclose(result, expected_dBm)
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_dBm)
    else:
        assert result == pytest.approx(expected_dBm)

@pytest.mark.parametrize("value_lin, expected_special_value", [
    (0.0, -np.inf),  # lin2dB(0) + 30 is -inf
    (-1.0, np.nan),  # lin2dB(negative) + 30 is nan
    (np.array([0.0, -1.0]), np.array([-np.inf, np.nan])),
    ([0.0, -1.0], [-np.inf, np.nan]),
])
def test_lin2dBm_edge_cases(value_lin, expected_special_value):
    """Tests lin2dBm with edge cases like zero and negative inputs."""
    result = lin2dBm(value_lin)
    lin2dB_lin2dBm(result, expected_special_value)


# noinspection PyTypeChecker
def test_lin2dBm_error_handling():
    """Tests lin2dBm with invalid input types."""
    with pytest.raises(TypeError):
        lin2dBm("invalid")

# --- Test dB2lin function ---
@pytest.mark.parametrize("value_dB, expected_lin", [
    (0.0, 1.0),
    (10.0, 10.0),
    (20.0, 100.0),
    (-10.0, 0.1),
    (-30.0, 0.001),
    (np.array([0.0, 10.0]), np.array([1.0, 10.0])),
    ([0.0, 10.0], [1.0, 10.0]),
])
def test_dB2lin_normal_cases(value_dB, expected_lin):
    """Tests dB2lin with normal float, numpy array, and list inputs."""
    result = dB2lin(value_dB)
    if isinstance(result, list):
        assert np.allclose(result, expected_lin)
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_lin)
    else:
        assert result == pytest.approx(expected_lin)


# noinspection PyTypeChecker
def test_dB2lin_error_handling():
    """Tests dB2lin with invalid input types."""
    with pytest.raises(TypeError):
        dB2lin("invalid")

# --- Test dBm2lin function ---
@pytest.mark.parametrize("value_dBm, expected_lin", [
    (30.0, 1.0),
    (40.0, 10.0),
    (0.0, 0.001),
    (np.array([30.0, 0.0]), np.array([1.0, 0.001])),
    ([30.0, 0.0], [1.0, 0.001]),
])
def test_dBm2lin_normal_cases(value_dBm, expected_lin):
    """Tests dBm2lin with normal float, numpy array, and list inputs."""
    result = dBm2lin(value_dBm)
    if isinstance(result, list):
        assert np.allclose(result, expected_lin)
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_lin)
    else:
        assert result == pytest.approx(expected_lin)


# noinspection PyTypeChecker
def test_dBm2lin_error_handling():
    """Tests dBm2lin with invalid input types."""
    with pytest.raises(TypeError):
        dBm2lin("invalid")

# --- Test wavelength2frequency function ---
@pytest.mark.parametrize("wavelength, expected_freq", [
    (c, 1.0),  # Wavelength equal to speed of light -> 1 Hz
    (1.0, c),  # 1 meter wavelength -> c Hz
    (1e-6, c / 1e-6), # 1 micrometer wavelength
    (np.array([1.0, 1e-6], dtype=float), np.array([c, c / 1e-6], dtype=float)),
])
def test_wavelength2frequency_normal_cases(wavelength, expected_freq):
    """Tests wavelength2frequency with normal float and numpy array inputs."""
    result = wavelength2frequency(wavelength)
    if isinstance(result, np.ndarray):
        assert np.allclose(result, expected_freq)
    else:
        assert result == pytest.approx(expected_freq)

@pytest.mark.parametrize("wavelength", [
    0.0,
    np.array([1.0, 0.0]),
])
def test_wavelength2frequency_edge_cases_zero(wavelength):
    """Tests wavelength2frequency with zero wavelength, expecting ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        wavelength2frequency(wavelength)

@pytest.mark.parametrize("wavelength", [
    -1.0,
    np.array([1.0, -1.0]),
])
def test_wavelength2frequency_edge_cases_negative(wavelength):
    """Tests wavelength2frequency with negative wavelength, expecting ValueError from scipy."""
    with pytest.raises(ValueError): # scipy.constants.lambda2nu raises ValueError for negative input
        wavelength2frequency(wavelength)


# noinspection PyTypeChecker
def test_wavelength2frequency_error_handling():
    """Tests wavelength2frequency with invalid input types."""
    with pytest.raises(TypeError):
        wavelength2frequency("invalid")

# --- Test frequency2wavelength function ---
@pytest.mark.parametrize("freq, expected_wavelength", [
    (1.0, c),  # 1 Hz frequency -> c meters
    (c, 1.0),  # c Hz frequency -> 1 meter
    (c / 1e-6, 1e-6), # c / 1e-6 Hz frequency -> 1 micrometer
    (np.array([1.0, c / 1e-6]), np.array([c, 1e-6])),
])
def test_frequency2wavelength_normal_cases(freq, expected_wavelength):
    """Tests frequency2wavelength with normal float and numpy array inputs."""
    result = frequency2wavelength(freq)
    if isinstance(result, np.ndarray):
        assert np.allclose(result, expected_wavelength)
    else:
        assert result == pytest.approx(expected_wavelength)

@pytest.mark.parametrize("freq", [
    0.0,
    np.array([1.0, 0.0]),
])
def test_frequency2wavelength_edge_cases_zero(freq):
    """Tests frequency2wavelength with zero frequency, expecting ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        frequency2wavelength(freq)

@pytest.mark.parametrize("freq", [
    -1.0,
    np.array([1.0, -1.0]),
])
def test_frequency2wavelength_edge_cases_negative(freq):
    """Tests frequency2wavelength with negative frequency, expecting ValueError from scipy."""
    with pytest.raises(ValueError): # scipy.constants.nu2lambda raises ValueError for negative input
        frequency2wavelength(freq)


# noinspection PyTypeChecker
def test_frequency2wavelength_error_handling():
    """Tests frequency2wavelength with invalid input types."""
    with pytest.raises(TypeError):
        frequency2wavelength("invalid")

# --- Test delta_frequency2delta_wavelength function ---
@pytest.mark.parametrize("delta_f, frequency, expected_delta_wl", [
    (1e6, 1e9, 1e6 * (c / 1e9) / 1e9), # delta_f * (lambda / nu)
    (0.0, 1e9, 0.0),
    (1e6, c, 1e6 * (1.0 / c)), # frequency = c, wavelength = 1
])
def test_delta_frequency2delta_wavelength_normal_cases(delta_f, frequency, expected_delta_wl):
    """Tests delta_frequency2delta_wavelength with normal inputs."""
    result = delta_frequency2delta_wavelength(delta_f, frequency)
    assert result == pytest.approx(expected_delta_wl)

@pytest.mark.parametrize("delta_f, frequency", [
    (1e6, 0.0), # Division by zero frequency
])
def test_delta_frequency2delta_wavelength_edge_cases_zero_frequency(delta_f, frequency):
    """Tests delta_frequency2delta_wavelength with zero frequency, expecting ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        delta_frequency2delta_wavelength(delta_f, frequency)

@pytest.mark.parametrize("delta_f, frequency", [
    (1e6, -1e9), # Negative frequency
])
def test_delta_frequency2delta_wavelength_edge_cases_negative_frequency(delta_f, frequency):
    """Tests delta_frequency2delta_wavelength with negative frequency, expecting ValueError."""
    with pytest.raises(ValueError): # From wavelength2frequency
        delta_frequency2delta_wavelength(delta_f, frequency)


# noinspection PyTypeChecker
def test_delta_frequency2delta_wavelength_error_handling():
    """Tests delta_frequency2delta_wavelength with invalid input types."""
    with pytest.raises(TypeError):
        delta_frequency2delta_wavelength("invalid", 1e9)
    with pytest.raises(TypeError):
        delta_frequency2delta_wavelength(1e6, "invalid")

# --- Test delta_wavelength2delta_frequency function ---
@pytest.mark.parametrize("delta_wl, wavelength, expected_delta_f", [
    (1e-9, 1e-6, 1e-9 * (c / 1e-6) / 1e-6), # delta_wl * (nu / lambda)
    (0.0, 1e-6, 0.0),
    (1e-9, c, 1e-9 * (1.0 / c)), # wavelength = c, frequency = 1
])
def test_delta_wavelength2delta_frequency_normal_cases(delta_wl, wavelength, expected_delta_f):
    """Tests delta_wavelength2delta_frequency with normal inputs."""
    result = delta_wavelength2delta_frequency(delta_wl, wavelength)
    assert result == pytest.approx(expected_delta_f)

@pytest.mark.parametrize("delta_wl, wavelength", [
    (1e-9, 0.0), # Division by zero wavelength
])
def test_delta_wavelength2delta_frequency_edge_cases_zero_wavelength(delta_wl, wavelength):
    """Tests delta_wavelength2delta_frequency with zero wavelength, expecting ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        delta_wavelength2delta_frequency(delta_wl, wavelength)

@pytest.mark.parametrize("delta_wl, wavelength", [
    (1e-9, -1e-6), # Negative wavelength
])
def test_delta_wavelength2delta_frequency_edge_cases_negative_wavelength(delta_wl, wavelength):
    """Tests delta_wavelength2delta_frequency with negative wavelength, expecting ValueError."""
    with pytest.raises(ValueError): # From frequency2wavelength
        delta_wavelength2delta_frequency(delta_wl, wavelength)


# noinspection PyTypeChecker
def test_delta_wavelength2delta_frequency_error_handling():
    """Tests delta_wavelength2delta_frequency with invalid input types."""
    with pytest.raises(TypeError):
        delta_wavelength2delta_frequency("invalid", 1e-6)
    with pytest.raises(TypeError):
        delta_wavelength2delta_frequency(1e-9, "invalid")

# --- Test convert_snr function ---
@pytest.mark.parametrize("snr_dB, actual_baud_rate, new_baud_rate, expected_snr_dB", [
    (10.0, 10e9, 12.5e9, 10.0 - lin2dB(12.5e9 / 10e9)), # Normal case
    (10.0, 10e9, 10e9, 10.0), # Same baud rate, no change
    (0.0, 10e9, 12.5e9, 0.0 - lin2dB(12.5e9 / 10e9)), # SNR of 0 dB
    (10.0, 10e9, DEFAULT_BAUD_RATE, 10.0 - lin2dB(DEFAULT_BAUD_RATE / 10e9)), # Using default new_baud_rate
    (np.array([10.0, 20.0]), np.array([10e9, 20e9]), 12.5e9,
     np.array([10.0 - lin2dB(12.5e9 / 10e9), 20.0 - lin2dB(12.5e9 / 20e9)])), # Array inputs
    ([10.0, 20.0], [10e9, 20e9], 12.5e9, [10.0 - lin2dB(12.5e9 / 10e9), 20.0 - lin2dB(12.5e9 / 20e9)]), # List inputs
])
def test_convert_snr_normal_cases(snr_dB, actual_baud_rate, new_baud_rate, expected_snr_dB):
    """Tests convert_snr with normal float, numpy array, and list inputs."""
    result = convert_snr(snr_dB, actual_baud_rate, new_baud_rate)
    if isinstance(result, list):
        assert np.allclose(result, expected_snr_dB)
    elif isinstance(result, np.ndarray):
        assert np.allclose(result, expected_snr_dB)
    else:
        assert result == pytest.approx(expected_snr_dB)

@pytest.mark.parametrize("snr_dB, actual_baud_rate, new_baud_rate, expected_special_value", [
    (10.0, 0.0, 12.5e9, -np.inf), # Division by zero actual_baud_rate -> lin2dB(inf) -> -inf
    (10.0, 12.5e9, 0.0, np.inf), # new_baud_rate is zero -> lin2dB(0) -> -inf. snr_dB - (-inf) = inf
    (10.0, -10e9, 12.5e9, np.nan), # Negative actual_baud_rate -> lin2dB(negative) -> nan
    (10.0, 10e9, -12.5e9, np.nan), # Negative new_baud_rate -> lin2dB(negative) -> nan
])
def test_convert_snr_edge_cases(snr_dB, actual_baud_rate, new_baud_rate, expected_special_value):
    """Tests convert_snr with edge cases like zero or negative baud rates."""
    result = convert_snr(snr_dB, actual_baud_rate, new_baud_rate)
    if np.isinf(expected_special_value):
        assert np.isinf(result) and np.sign(result) == np.sign(expected_special_value)
    elif np.isnan(expected_special_value):
        assert np.isnan(result)
    else:
        assert result == pytest.approx(expected_special_value)


# noinspection PyTypeChecker
def test_convert_snr_error_handling():
    """Tests convert_snr with invalid input types."""
    with pytest.raises(TypeError):
        convert_snr("invalid", 10e9, 12.5e9)
    with pytest.raises(TypeError):
        convert_snr(10.0, "invalid", 12.5e9)
    with pytest.raises(TypeError):
        convert_snr(10.0, 10e9, "invalid")

# --- Test binary_to_hex function ---
@pytest.mark.parametrize("binary_str, same_length, expected_hex", [
    ("0000", True, "0"),
    ("0001", True, "1"),
    ("1010", True, "a"),
    ("1111", True, "f"),
    ("00001111", True, "0f"),
    ("11110000", True, "f0"),
    ("1010101010101010", True, "aaaa"),
    ("0", True, "0"), # Single bit, padded to 4 bits then converted
    ("1", True, "1"), # Single bit, padded to 4 bits then converted
    ("10", True, "2"), # 2 bits, padded to 4 bits
    ("101", True, "5"), # 3 bits, padded to 4 bits
    ("11111111", True, "ff"), # 8 bits
    ("0000", False, "0"),
    ("0001", False, "1"),
    ("1010", False, "a"),
    ("1111", False, "f"),
    ("00001111", False, "f"), # Leading zeros removed
    ("11110000", False, "f0"),
    ("1", False, "1"),
    ("10", False, "2"),
    ("101", False, "5"),
    ("00000000", True, "00"), # All zeros, same_length
    ("00000000", False, "0"), # All zeros, not same_length
])
def test_binary_to_hex_normal_cases(binary_str, same_length, expected_hex):
    """Tests binary_to_hex with various binary strings and same_length options."""
    assert binary_to_hex(binary_str, same_length) == expected_hex


# noinspection PyTypeChecker
@pytest.mark.parametrize("binary_str", [
    "", # Empty string
    "1012", # Invalid binary digit
    "abc", # Non-binary characters
    "101 010", # Space in string
])
def test_binary_to_hex_error_handling(binary_str):
    """Tests binary_to_hex with invalid binary strings, expecting ValueError."""
    with pytest.raises(ValueError):
        binary_to_hex(binary_str)
    with pytest.raises(TypeError):
        binary_to_hex(123) # Non-string input

# --- Test hex_to_binary function ---
@pytest.mark.parametrize("hex_str, same_length, expected_binary", [
    ("0", True, "0000"),
    ("1", True, "0001"),
    ("a", True, "1010"),
    ("f", True, "1111"),
    ("0f", True, "00001111"),
    ("f0", True, "11110000"),
    ("aaaa", True, "1010101010101010"),
    ("0", False, "0"),
    ("1", False, "1"),
    ("a", False, "1010"),
    ("f", False, "1111"),
    ("0f", False, "1111"), # Leading zeros removed
    ("f0", False, "11110000"),
    ("00", True, "00000000"),
    ("00", False, "0"),
])
def test_hex_to_binary_normal_cases(hex_str, same_length, expected_binary):
    """Tests hex_to_binary with various hexadecimal strings and same_length options."""
    assert hex_to_binary(hex_str, same_length) == expected_binary


# noinspection PyTypeChecker
@pytest.mark.parametrize("hex_str", [
    "", # Empty string
    "g", # Invalid hex digit
    "12z", # Non-hex characters
    "1 2", # Space in string
])
def test_hex_to_binary_error_handling(hex_str):
    """Tests hex_to_binary with invalid hexadecimal strings, expecting ValueError."""
    with pytest.raises(ValueError):
        hex_to_binary(hex_str)
    with pytest.raises(TypeError):
        hex_to_binary(123) # Non-string input

# --- Test decimal_to_dms function ---
@pytest.mark.parametrize("decimal_degree, expected_dms", [
    (45.5, (45, 30, 0)),
    (45.75, (45, 45, 0)),
    (45.125, (45, 7, 30)),
    (0.0, (0, 0, 0)),
    (90.0, (90, 0, 0)),
    (-45.5, (-45, -30, -0)), # Minutes and seconds should reflect the sign of the original decimal
    (-45.75, (-45, -45, -0)),
    (-0.125, (0, -7, -30)),
    (180.0, (180, 0, 0)),
    (179.999999, (179, 59, 60)), # Rounding seconds
    (179.99999999999999, (180, 0, 0)), # Very close to 180, rounding
    (0.0000000000000001, (0, 0, 0)), # Very small positive
    (-0.0000000000000001, (0, 0, 0)), # Very small negative
])
def test_decimal_to_dms_normal_cases(decimal_degree, expected_dms):
    """Tests decimal_to_dms with various decimal degree inputs."""
    result = decimal_to_dms(decimal_degree)
    assert result == expected_dms


# noinspection PyTypeChecker
def test_decimal_to_dms_error_handling():
    """Tests decimal_to_dms with invalid input types."""
    with pytest.raises(TypeError):
        decimal_to_dms("invalid")
    with pytest.raises(TypeError):
        decimal_to_dms(None)

# --- Test dms_to_decimal function ---
@pytest.mark.parametrize("degrees, minutes, seconds, expected_decimal", [
    (45, 30, 0, 45.5),
    (45, 45, 0, 45.75),
    (45, 7, 30, 45.125),
    (0, 0, 0, 0.0),
    (90, 0, 0, 90.0),
    (-45, 30, 0, -45.5), # Negative degrees
    (45, -30, 0, -45.5), # Negative minutes
    # (45, 30, -0, -45.5), # Negative seconds
    (-45, -30, -0, -45.5), # All negative
    (180, 0, 0, 180.0),
    (0, 59, 60, 1.0), # 60 seconds is 1 minute
    (0, 0, 3600, 1.0), # 3600 seconds is 1 degree
    (0, 60, 0, 1.0), # 60 minutes is 1 degree
])
def test_dms_to_decimal_normal_cases(degrees, minutes, seconds, expected_decimal):
    """Tests dms_to_decimal with various degree, minute, second inputs."""
    result = dms_to_decimal(degrees, minutes, seconds)
    assert result == pytest.approx(expected_decimal)

@pytest.mark.parametrize("degrees, minutes, seconds", [
    (0, 0, 0.5), # Fractional seconds (should be int)
    (0, 0.5, 0), # Fractional minutes (should be int)
    (0.5, 0, 0), # Fractional degrees (should be int)
])
def test_dms_to_decimal_type_error_for_non_int_dms(degrees, minutes, seconds):
    """Tests dms_to_decimal with non-integer DMS components, expecting TypeError."""
    with pytest.raises(TypeError):
        dms_to_decimal(degrees, minutes, seconds)


# noinspection PyTypeChecker
def test_dms_to_decimal_error_handling():
    """Tests dms_to_decimal with invalid input types."""
    with pytest.raises(TypeError):
        dms_to_decimal("invalid", 0, 0)
    with pytest.raises(TypeError):
        dms_to_decimal(0, "invalid", 0)
    with pytest.raises(TypeError):
        dms_to_decimal(0, 0, "invalid")
    with pytest.raises(TypeError):
        dms_to_decimal(None, 0, 0)