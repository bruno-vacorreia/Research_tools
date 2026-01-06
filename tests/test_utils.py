import pytest
import numpy as np
import pandas as pd
from research_tools import utils
import warnings

@pytest.mark.parametrize("default, new, expected", [({'a': 1, 'b': 2}, {'b': 3, 'c': 4}, {'a': 1, 'b': 3, 'c': 4})])
def test_update_default_dict(default, new, expected):
    """Tests update_default_dict merges and overrides keys correctly."""
    result = utils.update_default_dict(default, new)
    assert result == expected
    assert default == {'a': 1, 'b': 2}  # Ensure original is not modified

@pytest.mark.parametrize("input_dict, expected_shape", [({'x': np.array([[1, 2]]), 'y': 5}, (2,))])
def test_squeeze_dict(input_dict, expected_shape):
    """Tests squeeze_dict squeezes numpy arrays in dict values."""
    result = utils.squeeze_dict(input_dict)
    assert isinstance(result['x'], np.ndarray)
    assert result['x'].shape == expected_shape
    assert result['y'] == 5

@pytest.mark.parametrize("d", [({'a': 1, 'b': 2.5, 'c': 'str', 'd': True, 'e': None})])
def test_format_dict_json_basic_types(d):
    """Tests format_dict_json with basic types."""
    result = utils.format_dict_json(d)
    assert result == d

@pytest.mark.parametrize("d, expected", [
    ({'a': np.int32(5), 'b': np.float64(2.5), 'c': np.array([1, 2, 3]), 'd': {'e': np.float16(1.2)}},
     {'a': 5, 'b': 2.5, 'c': [1, 2, 3], 'd': {'e': float(np.float16(1.2))}})
])
def test_format_dict_json_numpy_types(d, expected):
    """Tests format_dict_json with numpy types and nested dicts."""
    result = utils.format_dict_json(d)
    assert result == expected
    class Dummy: pass
    with pytest.raises(TypeError):
        utils.format_dict_json({'x': Dummy()})

@pytest.mark.parametrize("values, expected_dtype", [
    (['a', 'a', 'b', 'c', 'a', 'a', 'a', 'a', 'a', 'a'], 'category')
])
def test_reduce_df_size_category(values, expected_dtype):
    """Tests reduce_df_size converts object columns to category when appropriate."""
    df = pd.DataFrame({'col': values})
    reduced = utils.reduce_df_size(df.copy())
    assert isinstance(reduced['col'].dtype, pd.CategoricalDtype)

@pytest.mark.parametrize("values, expected_dtypes", [
    ([1, 2, 3, 4, 5], ['int8', 'int16', 'int32', 'uint8', 'uint16', 'uint32'])
])
def test_reduce_df_size_int_downcast(values, expected_dtypes):
    """Tests reduce_df_size downcasts integer columns."""
    df = pd.DataFrame({'col': values})
    reduced = utils.reduce_df_size(df.copy())
    assert str(reduced['col'].dtype) in expected_dtypes

@pytest.mark.parametrize("values, expected_dtypes", [
    ([1.0, 2.0, 3.0, 4.0, 5.0], ['float16', 'float32'])
])
def test_reduce_df_size_float_downcast(values, expected_dtypes):
    """Tests reduce_df_size downcasts float columns."""
    df = pd.DataFrame({'col': values})
    reduced = utils.reduce_df_size(df.copy())
    assert str(reduced['col'].dtype) in expected_dtypes

@pytest.mark.parametrize("df_dict, expected_datetime_cols, expected_object_cols", [
    (
        {
            'date': [
                '2020-01-01', '2021-02-02', '2022-03-03', '2023-04-04', '2024-05-05',
                '2025-06-06', '2026-07-07', '2027-08-08', '2028-09-09', '2029-10-10',
                '2030-11-11', '2031-12-12', '2032-01-13', '2033-02-14', '2034-03-15'
            ],
            'datetime': [
                '2020-01-01 10:00', '2021-02-02 12:30', '2022-03-03 15:45', '2023-04-04 08:15', '2024-05-05 20:20',
                '2025-06-06 14:10', '2026-07-07 09:05', '2027-08-08 23:59', '2028-09-09 00:00', '2029-10-10 16:45',
                '2030-11-11 11:11', '2031-12-12 12:12', '2032-01-13 13:13', '2033-02-14 14:14', '2034-03-15 15:15'
            ],
            'timestamp': [
                '2020-01-01T00:00:00', '2021-02-02T00:00:00', '2022-03-03T00:00:00', '2023-04-04T00:00:00', '2024-05-05T00:00:00',
                '2025-06-06T00:00:00', '2026-07-07T00:00:00', '2027-08-08T00:00:00', '2028-09-09T00:00:00', '2029-10-10T00:00:00',
                '2030-11-11T00:00:00', '2031-12-12T00:00:00', '2032-01-13T00:00:00', '2033-02-14T00:00:00', '2034-03-15T00:00:00'
            ],
            'time': [
                '10:00', '12:30', '15:45', '08:15', '20:20',
                '14:10', '09:05', '23:59', '00:00', '16:45',
                '11:11', '12:12', '13:13', '14:14', '15:15'
            ],
            'not_a_date': [
                'foo', 'bar', 'baz', 'qux', 'quux',
                'corge', 'grault', 'garply', 'waldo', 'fred',
                'plugh', 'xyzzy', 'thud', 'spam', 'eggs'
            ]
        },
        ['date', 'datetime', 'timestamp'],
        ['not_a_date']
    )
])
def test_reduce_df_size_datetime_casting(df_dict, expected_datetime_cols, expected_object_cols):
    """Tests reduce_df_size converts date-like columns to datetime dtype."""
    import warnings
    df = pd.DataFrame(df_dict)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        reduced = utils.reduce_df_size(df.copy())
    for col in expected_datetime_cols:
        assert pd.api.types.is_datetime64_any_dtype(reduced[col]), f"Column {col} not converted to datetime"
    for col in expected_object_cols:
        assert reduced[col].dtype == 'object'
    # Test with invalid date formats
    df_invalid = pd.DataFrame({'date': df['not_a_date'].values})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        reduced_invalid = utils.reduce_df_size(df_invalid.copy())
    assert reduced_invalid['date'].dtype == 'object'
