"""
Module containing utility functions for data manipulation.
"""
import numpy as np
from numpy import squeeze, ndarray
from pandas import DataFrame, to_numeric
from typing import Union, List, Dict, Any, Tuple, Literal

FIXED_PERCENTAGE_CATEGORY = 0.1
LIST_INTEGERS_TYPES = [int, np.int_, np.intc, np.intp,
                       np.int8, np.int16, np.int32, np.int64,
                       np.uint8, np.uint16, np.uint32, np.uint64]
LIST_FLOAT_TYPES = [float, np.float16, np.float32, np.float64]


def update_default_dict(default_dict: dict, new_dict: dict) -> dict:
    """
    Update the default function parameters dict with new values of another dict.
    If a key is not in the new dict, the default parameters of the default dict will be used.

    :param default_dict: Dict of default parameters
    :param new_dict: Dict of new parameters
    :return: Updated dict with new parameters
    """
    new_default_dict = default_dict.copy()
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
        value_type = type(value)
        if value_type in LIST_FLOAT_TYPES:
            new_dict[key] = float(value)
        elif value_type in LIST_INTEGERS_TYPES:
            new_dict[key] = int(value)
        elif value_type is ndarray:
            new_dict[key] = value.tolist()
        elif value_type is dict:
            new_dict[key] = format_dict_json(value)
        elif value_type in [list, str, bool] or value is None:
            new_dict[key] = value
        else:
            raise TypeError(f'Unsupported type for value in dict: {value_type}')
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
        # input_df[column].fillna('Not valid')
        if (input_df[column].describe()['freq'] / input_df[column].describe()['count']) > FIXED_PERCENTAGE_CATEGORY:
            input_df[column] = input_df[column].astype('category')

    # Reduce the size of int64 types by converting them to smaller int types
    for column in input_df.select_dtypes(include='int64').columns:
        input_df[column] = to_numeric(input_df[column], downcast='signed' if input_df[column].min() < 0 else 'unsigned')

    # Reduce the size of float64 types by converting them to smaller float types
    for column in input_df.select_dtypes(include='float64').columns:
        input_df[column] = to_numeric(input_df[column], downcast='float')

    return input_df
