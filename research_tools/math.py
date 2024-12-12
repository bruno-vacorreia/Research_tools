"""
Module containing functions for mathematical operations.
"""
from numpy import seterr, array, sum
from numpy.random import normal, Generator

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
    if generator is None:
        value = normal(mean, sigma)
    else:
        value = generator.normal(mean, sigma)

    return value


if __name__ == '__main__':
    import research_tools.plot as plt

    # Example of SNR sum
    test_list = [41.76, 42.9, 40.06]
    test_array = array(test_list)
    print(round(snr_dB_sum(test_list), 2))
    print(round(snr_dB_sum(test_array), 2))

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
