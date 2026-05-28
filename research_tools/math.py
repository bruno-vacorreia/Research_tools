"""
Module containing mathematical utilities for research and signal-processing workflows.

Includes reciprocal-SNR combination in decibels, bounded normal random sampling, and great-circle
distance between geographic coordinates.
"""
from numpy import seterr, array, asarray, ndarray, round as np_round
from numpy.random import normal, Generator
from math import sin, cos, asin, sqrt, radians
from typing import Union, Optional

from research_tools.conversions import lin2dB, dB2lin
from research_tools.constants import RADIUS_EARTH_KM

seterr(divide='ignore')


def snr_dB_sum(*args: Union[float, list, ndarray]) -> Union[float, ndarray]:
    """
    Combine independent SNR contributions given in decibels (dB).

    Each argument is converted to linear SNR, summed in the reciprocal-noise domain
    (``1/SNR_lin``), then converted back to dB via :func:`research_tools.conversions.lin2dB`.
    Accepts scalars, lists, or NumPy arrays; array inputs are broadcast element-wise.

    :param args: One or more SNR values in dB to combine.
    :return: Combined SNR in dB, with the same shape as the array inputs when arrays are used.
    """
    snr_list = [1 / dB2lin(asarray(arg)) for arg in args]
    snr_sum = sum(snr_list)

    return lin2dB(1 / snr_sum)


def snr_dB_subtract(combined: Union[float, list, ndarray],
                    *args: Union[float, list, ndarray]) -> Union[float, ndarray]:
    """
    Remove one or more SNR contributions (in dB) from a combined SNR.

    Uses the same reciprocal-SNR model as :func:`snr_dB_sum`. If ``combined`` equals
    ``snr_dB_sum(*parts)`` for independent noise terms, then ``snr_dB_subtract(combined, *q)``
    returns the SNR in dB for the merge of ``parts`` with every element of ``q`` removed;
    the order of ``q`` does not matter.

    :param combined: Combined SNR in dB (typically from :func:`snr_dB_sum`).
    :param args: One or more SNR values in dB to subtract from the combined reciprocal-noise budget.
    :return: Resulting SNR in dB after subtraction in the reciprocal domain.
    """
    inv_snr = 1 / dB2lin(asarray(combined))
    for arg in args:
        inv_snr -= 1 / dB2lin(asarray(arg))

    return lin2dB(1 / inv_snr)


def normal_distribution_3_sigma(mean: float = 0.0, minimum: float = -2.0, maximum: float = 2.0,
                                generator: Optional[Generator] = None) -> float:
    """
    Draw a single sample from a normal distribution defined by a three-sigma range.

    The interval ``[minimum, maximum]`` is treated as mean ± 3σ, so
    ``σ = (maximum - minimum) / 6``. Useful for modeling bounded random effects (e.g. splice loss)
    when only the expected spread is known.

    :param mean: Mean of the normal distribution.
    :param minimum: Lower bound of the three-sigma range (μ − 3σ).
    :param maximum: Upper bound of the three-sigma range (μ + 3σ).
    :param generator: NumPy random generator for reproducible draws; if omitted,
        :func:`numpy.random.normal` is used.
    :return: One random sample from ``N(mean, σ)``.
    """
    # Calculate standard deviation using the 3-sigma rule
    sigma = (maximum - minimum) / 6

    # Generate a random value from the normal distribution
    distribution = normal(mean, sigma) if generator is None else generator.normal(mean, sigma)

    return distribution


def haversine_distance(sour_lat: float, sour_lon: float, dest_lat: float,
                       dest_lon: float) -> float:
    """
    Compute the great-circle distance between two points on Earth.

    Coordinates are given in decimal degrees. The result uses
    :data:`research_tools.constants.RADIUS_EARTH_KM` and is returned in kilometers.

    :param sour_lat: Latitude of the source point in degrees.
    :param sour_lon: Longitude of the source point in degrees.
    :param dest_lat: Latitude of the destination point in degrees.
    :param dest_lon: Longitude of the destination point in degrees.
    :return: Haversine distance in kilometers.
    """
    sour_lat, sour_lon, dest_lat, dest_lon = map(radians, [sour_lat, sour_lon, dest_lat, dest_lon])

    k = (sin((dest_lat - sour_lat) / 2) ** 2 +
         (cos(sour_lat) * cos(dest_lat)) * sin((dest_lon - sour_lon) / 2) ** 2)

    return 2 * RADIUS_EARTH_KM * asin(sqrt(k))


if __name__ == '__main__':
    import research_tools.plot as plt

    # Example of SNR sum
    first_list = [41.76, 42.9, 40.06]
    first_array = array(first_list)
    second_array = array([first_array, first_array - 1])
    second_list = [first_list, first_list, 35]

    print(f'SNR list: {first_list}')
    print(round(snr_dB_sum(*first_list), 2))

    print(f'SNR array: {first_array}')
    print(round(snr_dB_sum(*first_array), 2))

    print(f'SNR matrix: {second_array}')
    print(np_round(snr_dB_sum(*second_array), 2))

    print(f'SNR list with different sizes: {second_list}')
    print(np_round(snr_dB_sum(*second_list), 2))

    # Example of normal distribution
    num_values = int(1e5)
    num_bins = 40
    aux_minimum = 9.0
    aux_maximum = 11.0
    aux_mean = aux_minimum + ((aux_maximum - aux_minimum) / 2)
    splice_loss_list = list()
    for _ in range(num_values):
        splice_loss_list.append(normal_distribution_3_sigma(aux_mean, aux_minimum, aux_maximum))

    fig_normal = plt.get_figure(dpi=100)
    ax_normal = plt.add_subplot(fig_normal)
    ax_normal.hist(x=splice_loss_list, bins=num_bins)
    plt.set_labels(axis=ax_normal, x_label='Value', y_label='Number')
    plt.set_ticks(axis=ax_normal)
    fig_normal.tight_layout()

    plt.show()
