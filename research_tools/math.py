"""
Module containing functions for mathematical operations.
"""
from numpy import seterr, array, asarray, ndarray, round as np_round
from numpy.random import normal, Generator
from math import sin, cos, asin, sqrt, radians
from typing import Union

from research_tools.conversions import lin2dB, dB2lin
from research_tools.constants import RADIUS_EARTH_KM

seterr(divide='ignore')


def snr_dB_sum(*args) -> Union[float, ndarray]:
    """
    Calculate the sum of Signal-to-Noise Ratios (SNR) given in decibels (dB).

    :param args: Variable length argument list of SNR values in dB.
    :return: The combined SNR in dB.
    """
    snr_list = [1 / dB2lin(asarray(arg)) for arg in args]
    snr_sum = sum(snr_list)

    return lin2dB(1 / snr_sum)


def normal_distribution_3_sigma(mean=0.0, minimum=-2.0, maximum=2.0, generator: Generator = None) -> float:
    """
    Function to generate a normal distribution with 3 standard deviations.

    :param mean: Normal distribution mean
    :param minimum: Normal distribution minimum
    :param maximum: Normal distribution maximum
    :param generator: Random generator to produce the distribution. If not provided, the numpy default generator is
    used.
    :return: Normal distribution value
    """
    # Calculate standard deviation using the 3-sigma rule
    sigma = (maximum - minimum) / 6

    # Generate a random value from the normal distribution
    distribution = normal(mean, sigma) if generator is None else generator.normal(mean, sigma)

    return distribution


def haversine_distance(sour_lat, sour_lon, dest_lat, dest_lon) -> float:
    """
    Computes the Haversine distance between two points.

    :param sour_lat: Latitude of point 1
    :param sour_lon: Longitude of point 1
    :param dest_lat: Latitude of point 2
    :param dest_lon: Longitude of point 2
    :return: Haversine distance
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
