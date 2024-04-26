import numpy as np
from numpy import squeeze, ndarray
from pandas import DataFrame, to_numeric

from typing import Union, List, Tuple, Dict, Literal, Any
from collections.abc import Iterable

FIXED_PERCENTAGE_CATEGORY = 0.1
LIST_FLOAT_TYPES = [np.float32]


def update_default_dict(default_dict: dict, new_dict: dict) -> dict:
    """
    Update the default function parameters dict with new values of another dict.
    If key is not in the new dict, the default parameters of the default dict will be used.

    :param default_dict: Dict of default parameters
    :param new_dict: Dict of new parameters
    :return: New created dict
    """
    new_default_dict = default_dict.copy()
    for key in new_dict.keys():
        new_default_dict[key] = new_dict[key]

    return new_default_dict


def squeeze_dict(input_dict: dict) -> dict:
    """
    Squeeze all arrays within a dict

    :param input_dict: Original dict
    :return: New squeezed dict
    """
    new_dict = {key: squeeze(value) if isinstance(value, ndarray) else value for key, value in input_dict.items()}

    return new_dict


def format_dict_json(input_dict: dict) -> dict:
    """
    Format dictionary in order to save as json file.

    :param input_dict: Input dictionary
    :return: Formatted dictionary
    """
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, (np.float_, np.float16, np.float32, np.float64)):
            new_dict[key] = float(value)
        elif isinstance(value, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8,
                                np.uint16, np.uint32, np.uint64)):
            new_dict[key] = int(value)
        elif isinstance(value, ndarray):
            new_dict[key] = value.tolist()
        elif isinstance(value, dict):
            new_dict[key] = format_dict_json(value)
        elif isinstance(value, list):
            new_dict[key] = value
        else:
            raise TypeError('Unsupported type for value in dict')

    return new_dict


def reduce_df_size(input_df: DataFrame):
    """
    Change the type of each column based on its types/values, in order to reduce the data frame memory size.
    Working for category, integer and float values.

    :param input_df: Input dataframe
    :return: Reduced dataframe
    """
    # TODO: Implement a logic in order to cast to date-time type by the column name. Do it before the category casting.
    # Reduce the size of the object types, trying to convert them to category
    for column in input_df.select_dtypes(include='object').columns:
        # input_df[column].fillna('Not valid')
        if (input_df[column].describe()['freq'] / input_df[column].describe()['count']) > FIXED_PERCENTAGE_CATEGORY:
            input_df[column] = input_df[column].astype('category')

    # Reduce the size of the int64 types, trying to convert them to reduced size ints
    for column in input_df.select_dtypes(include='int64').columns:
        min_value = input_df[column].min()
        if min_value < 0:
            input_df[column] = to_numeric(input_df[column], downcast='signed')
        else:
            input_df[column] = to_numeric(input_df[column], downcast='unsigned')

    # Reduce the size of the float64 types, trying to convert them to reduced size floats
    for column in input_df.select_dtypes(include='float64').columns:
        # Applies the regular downcast function to float type
        input_df[column] = to_numeric(input_df[column], downcast='float')

        # TODO: Check this part, as the resolution of float32 is 1e-06 while the resolution of float 64 is 1e-15
        # Forces the columns to downcast if the minimum and maximum values are meet (float32 has resolution of 1e-6)
        # max_value, min_value = input_df[column].max(), input_df[column].min()
        # for float_type in LIST_FLOAT_TYPES:
        #     type_info = np.finfo(float_type)
        #     if min_value >= type_info.min and max_value <= type_info.max:
        #         input_df[column] = input_df[column].astype(float_type)
        #         break

    return input_df
