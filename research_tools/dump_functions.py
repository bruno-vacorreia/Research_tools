"""
Module containing dumb functions, used for debugging purposes.
"""
from numpy import random
from time import sleep


def random_generation_wait_arg(arg):
    low, high = arg
    random_value = round(random.uniform(low=low, high=high), 3)
    if 2 < random_value < 3.1:
        raise ValueError('test error message is appearing')
    print('Waiting {} seconds'.format(random_value))
    sleep(random_value)
    return random_value


def random_generation_wait_param(low, high):
    random_value = round(random.uniform(low=low, high=high), 3)
    print('Waiting {} seconds'.format(random_value))
    sleep(random_value)
    return random_value
