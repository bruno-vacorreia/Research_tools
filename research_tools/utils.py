"""
Module containing utility functions for data manipulation.
"""
from numpy import (squeeze, ndarray, int_, intc, intp, int8, int16, int32, int64, uint8, uint16, uint32, uint64,
                   float16, float32, float64)
from pandas import DataFrame, to_numeric
from copy import deepcopy


FIXED_PERCENTAGE_CATEGORY = 0.1
"""Percentage threshold to convert object type to category type in dataframe columns."""
LIST_INTEGERS_TYPES = tuple([int, int_, intc, intp,
                             int8, int16, int32, int64,
                             uint8, uint16, uint32, uint64])
"""Tuple of integer types."""
LIST_FLOAT_TYPES = tuple([float, float16, float32, float64])
"""Tuple of float types."""


def update_default_dict(default_dict: dict, new_dict: dict) -> dict:
    """
    Update the default function parameters dict with new values of another dict.
    If a key is not in the new dict, the default parameters of the default dict will be used.

    :param default_dict: Dict of default parameters
    :param new_dict: Dict of new parameters
    :return: Updated dict with new parameters
    """
    new_default_dict = deepcopy(default_dict)
    new_default_dict.update(new_dict)

    return new_default_dict


def squeeze_dict(input_dict: dict) -> dict:
    """
    Squeeze all arrays within a dict.

    :param input_dict: Original dict
    :return: New dict with squeezed arrays
    """
    return {key: squeeze(value) if isinstance(value, ndarray) else value for key, value in input_dict.items()}


def format_dict_json(input_dict: dict) -> dict:
    """
    Format dictionary to save as a JSON file.

    :param input_dict: Input dictionary
    :return: Formatted dictionary
    """
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, LIST_FLOAT_TYPES):
            new_dict[key] = float(value)
        elif isinstance(value, LIST_INTEGERS_TYPES):
            new_dict[key] = int(value)
        elif isinstance(value, ndarray):
            new_dict[key] = value.tolist()
        elif isinstance(value, dict):
            new_dict[key] = format_dict_json(value)
        elif isinstance(value, (list, str, bool)) or value is None:
            new_dict[key] = value
        else:
            raise TypeError(f'Unsupported type for value in dict: {type(value)}')
    return new_dict


def reduce_df_size(input_df: DataFrame) -> DataFrame:
    """
    Change the type of each column based on its types/values to reduce the dataframe memory size.
    Works for category, integer, and float values.

    :param input_df: Input dataframe
    :return: Reduced dataframe
    """
    # TODO: Implement a logic in order to cast to date-time type by the column name. Do it before the category casting.
    # Reduce the size of object types by converting them to category
    for column in input_df.select_dtypes(include='object').columns:
        desc = input_df[column].describe()
        if (desc['freq'] / desc['count']) > FIXED_PERCENTAGE_CATEGORY:
            input_df[column] = input_df[column].astype('category')

    # Reduce the size of int64 types by converting them to smaller int types
    for column in input_df.select_dtypes(include='int64').columns:
        input_df[column] = to_numeric(input_df[column], downcast='signed' if input_df[column].min() < 0 else 'unsigned')

    # Reduce the size of float64 types by converting them to smaller float types
    for column in input_df.select_dtypes(include='float64').columns:
        input_df[column] = to_numeric(input_df[column], downcast='float')

    return input_df
