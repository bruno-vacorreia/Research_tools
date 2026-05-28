"""
Module containing general-purpose utilities for dictionaries and pandas DataFrames.

Supports merging default parameter dicts, preparing nested structures for JSON export,
squeezing NumPy arrays in dicts, and reducing DataFrame memory via dtype downcasting.
"""
from numpy import (squeeze, ndarray, int_, intc, intp, int8, int16, int32, int64, uint8, uint16, uint32, uint64,
                   float16, float32, float64)
from pandas import DataFrame, to_numeric, to_datetime
from copy import deepcopy


FIXED_PERCENTAGE_CATEGORY = 0.1
"""Minimum fraction of repeated values (``freq / count``) required to cast a string column to ``category``."""

LIST_INTEGERS_TYPES = tuple([int, int_, intc, intp,
                             int8, int16, int32, int64,
                             uint8, uint16, uint32, uint64])
"""Tuple of scalar integer types recognized by :func:`format_dict_json`."""

LIST_FLOAT_TYPES = tuple([float, float16, float32, float64])
"""Tuple of scalar float types recognized by :func:`format_dict_json`."""


def update_default_dict(default_dict: dict, new_dict: dict) -> dict:
    """
    Merge a default parameter dict with overrides without mutating the original.

    Deep-copies ``default_dict``, then applies ``new_dict`` with :meth:`dict.update`. Keys present only
    in ``default_dict`` are kept; keys in ``new_dict`` replace or add entries. Used throughout
    :mod:`research_tools.in_out` and :mod:`research_tools.plot` to combine module defaults with
    caller ``kwargs``.

    :param default_dict: Base parameters (e.g. save/load defaults).
    :param new_dict: Overrides supplied by the caller.
    :return: New dict containing the merged parameters.
    """
    new_default_dict = deepcopy(default_dict)
    new_default_dict.update(new_dict)

    return new_default_dict


def squeeze_dict(input_dict: dict) -> dict:
    """
    Remove length-1 dimensions from NumPy arrays stored in a dict.

    Non-array values are copied unchanged. Applied recursively only for ndarray values at the top
    level of ``input_dict`` (nested dicts are not walked). Used when preparing data for MATLAB
    ``.mat`` export in :mod:`research_tools.in_out`.

    :param input_dict: Mapping that may contain :class:`numpy.ndarray` values.
    :return: New dict with the same keys; array values passed through :func:`numpy.squeeze`.
    """
    return {key: squeeze(value) if isinstance(value, ndarray) else value for key, value in input_dict.items()}


def format_dict_json(input_dict: dict) -> dict:
    """
    Recursively convert a dict to JSON-serializable Python types.

    Preserves ``list``, ``str``, ``bool``, and ``None``. Converts nested dicts recursively,
    NumPy arrays to lists, and NumPy scalar integers and floats to built-in ``int`` and ``float``.
    Types outside this set raise :exc:`TypeError`.

    :param input_dict: Arbitrarily nested mapping to prepare for :func:`json.dump`.
    :return: New dict safe to serialize as JSON.
    :raises TypeError: If a value has an unsupported type.
    """
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, (list, str, bool)) or value is None:
            new_dict[key] = value
        elif isinstance(value, dict):
            new_dict[key] = format_dict_json(value)
        elif isinstance(value, ndarray):
            new_dict[key] = value.tolist()
        elif isinstance(value, LIST_FLOAT_TYPES):
            new_dict[key] = float(value)
        elif isinstance(value, LIST_INTEGERS_TYPES):
            new_dict[key] = int(value)
        else:
            raise TypeError(f'Unsupported type for value in dict: {type(value)}')
    return new_dict


def reduce_df_size(input_df: DataFrame) -> DataFrame:
    """
    Downcast DataFrame columns in place to reduce memory usage.

    Processing order:

    1. **Datetime** — Columns whose names contain ``date``, ``datetime``, ``timestamp``, or ``time``
       (case-insensitive) are parsed with :func:`pandas.to_datetime`. Unparseable columns are left
       unchanged and a message is printed.
    2. **Category** — Object or string columns where the most frequent value accounts for more than
       :data:`FIXED_PERCENTAGE_CATEGORY` of non-null rows are cast to ``category``.
    3. **Integers** — ``int64`` columns are downcast to the smallest signed or unsigned integer
       dtype that fits the data.
    4. **Floats** — ``float64`` columns are downcast with :func:`pandas.to_numeric`.

    :param input_df: DataFrame to optimize (modified in place).
    :return: The same DataFrame instance with reduced dtypes.
    """
    # Cast columns to datetime type by column name before category casting
    datetime_keywords = ['date', 'datetime', 'timestamp', 'time']
    for column in input_df.columns:
        if any(keyword in column.lower() for keyword in datetime_keywords):
            try:
                input_df[column] = to_datetime(input_df[column], errors='raise')
            except (ValueError, TypeError) as e:
                # TODO: Improve logic of the error handling
                print(f"Could not convert column '{column}' to datetime: {e}")

    # Reduce the size of object/string types by converting them to category
    for column in input_df.select_dtypes(include=['object', 'string']).columns:
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
