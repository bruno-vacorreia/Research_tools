"""
Module containing functions for input and output of data and for folder creation and paths.
"""
from pathlib import Path
from os.path import exists, isfile
from os import makedirs
from pprint import pformat
from pandas import read_csv, DataFrame, read_excel
from numpy import squeeze, ndarray, load as load_np, save as save_np, random
from json import load as load_json, dump as save_json
from scipy.io import loadmat as load_mat, savemat as save_mat

from research_tools.utils import update_default_dict, squeeze_dict, Union, format_dict_json, reduce_df_size

DEFAULT_CSV_PARAMS = {'index': False, }
DEFAULT_JSON_PARAMS = {'indent': 2, }
DEFAULT_PRETTY_PRINT_JSON_PARAMS = {'indent': 2, 'width': 120, 'compact': True, 'sort_dicts': False}
DEFAULT_NPY_PARAMS = {}
DEFAULT_MAT_PARAMS = {}
DEFAULT_EXCEL_PARAMS = {'header': True, 'index': False, }
PRETTY_PRINT_OPTION = True


def load(file_path: Union[Path, str], squeeze_arrays: bool = True, remove_matlab_keys: bool = True,
         downcast_type: bool = False, **kwargs) -> Union[dict, DataFrame, ndarray]:
    """
    Load main types of data used in our work.

    :param file_path: File path
    :param squeeze_arrays: Option to squeeze arrays within the dict (Used for numpy array and .mat files)
    :param remove_matlab_keys: Option to remove the Matlab parameters from the dict (Used for .mat files).
    True if the data should remove the Matlab information.
    :param downcast_type: Option to apply a downcast function to the data (Used for .csv and Excel files)
    :param kwargs: Parameters of the respective load function
    :return: Data loaded
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if file_path.suffix in ['.json']:
        file = open(file_path, 'r')
        data = load_json(file, **kwargs)
        file.close()
    elif file_path.suffix in ['.csv']:
        data = read_csv(filepath_or_buffer=file_path, **kwargs)
        if downcast_type:
            data = reduce_df_size(data)
    elif file_path.suffix in ['.mat']:
        data = load_mat(file_name=str(file_path), **kwargs)
        if squeeze_arrays:
            data = squeeze_dict(data)
        if remove_matlab_keys:
            for key in ['__header__', '__version__', '__globals__']:
                data.pop(key, None)
    elif file_path.suffix in ['.npy', '.npz']:
        data = load_np(file=file_path, **kwargs)
        if squeeze_arrays:
            data = squeeze(data)
    elif file_path.suffix in ['.xlsx', '.xls', '.ods']:
        data = read_excel(io=file_path, **kwargs)
        if downcast_type:
            data = reduce_df_size(data)
    else:
        raise TypeError('Load function not implemented for "{}" type'.format(file_path.suffix))

    return data


def save(file_path: Union[Path, str], data: Union[dict, DataFrame, ndarray],
         json_pretty_print: bool = PRETTY_PRINT_OPTION, **kwargs):
    """
    Save the main types of data used in our work.
    Using the default parameters of the respective save function, unless set different.

    :param file_path: File path
    :param data: Data to save
    :param json_pretty_print: Use the pretty print library to produce the json file
    :param kwargs: Parameters of the respective save function
    :return:
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if file_path.suffix in ['.json']:
        data = format_dict_json(data)
        file = open(file_path, 'w')
        if not json_pretty_print:
            save_json(obj=data, fp=file, **update_default_dict(DEFAULT_JSON_PARAMS, kwargs))
        else:
            data_str = pformat(data, **update_default_dict(DEFAULT_PRETTY_PRINT_JSON_PARAMS, kwargs))
            data_str = data_str.replace("'", '"')
            data_str = data_str.replace('None', 'null')
            file.write(data_str)
        file.close()
    elif file_path.suffix in ['.csv']:
        data.to_csv(path_or_buf=file_path, **update_default_dict(DEFAULT_CSV_PARAMS, kwargs))
    elif file_path.suffix in ['.mat']:
        save_mat(file_name=file_path, mdict=data, **update_default_dict(DEFAULT_MAT_PARAMS, kwargs))
    elif file_path.suffix in ['.npy', '.npz']:
        save_np(file=file_path, arr=data, **update_default_dict(DEFAULT_NPY_PARAMS, kwargs))
    elif file_path.suffix in ['.xlsx', '.xls', '.ods']:
        data.to_excel(excel_writer=file_path, **update_default_dict(DEFAULT_EXCEL_PARAMS, kwargs))
    else:
        raise TypeError('Save function not implemented for "{}" type'.format(file_path.suffix))


def get_or_create_folder(folder_path: Union[Path, str]) -> Path:
    """
    Creates entire folder path if it does not exist

    :param folder_path: Folder path
    :return: Same folder path, but with created folder if it does not exist.
    """
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    if not exists(folder_path):
        makedirs(folder_path)

    return folder_path


if __name__ == '__main__':
    save_option = True
    load_option = True
    error_invalid_type_option = False
    reduce_function_option = False

    # Save function for different data types
    if save_option:
        array_example = random.random((1, 10))
        dump_dict = {'array_1': random.random(10),
                     'array_2': array_example}
        save(Path('../dump_data/data_example.npy'), data=array_example)
        print('Finished saving as numpy array')
        save(Path('../dump_data/data_example.mat'), data=dump_dict, **{'do_compression': True})
        print('Finished saving as Matlab file')
        save(Path('../dump_data/data_example.json'), data=dump_dict, json_pretty_print=False)
        save(Path('../dump_data/data_example_pretty_print.json'), data=dump_dict, json_pretty_print=True)
        print('Finished saving as json')
        dump_dict = squeeze_dict(dump_dict)
        df = DataFrame.from_dict(data=dump_dict)
        save(Path('../dump_data/data_example.csv'), data=df)
        print('Finished saving as csv')
        save(Path('../dump_data/data_example.xls'), data=df)
        print('Finished saving as xls')
        save(Path('../dump_data/data_example.xlsx'), data=df)
        print('Finished saving as xlsx')
        save(Path('../dump_data/data_example.ods'), data=df)
        print('Finished saving as ods')

    # Load function for different data types
    if load_option:
        file_npy = load('../dump_data/data_example.npy', squeeze_arrays=True)
        print('Finished loading as numpy array')
        file_json = load('../dump_data/data_example.json')
        print('Finished loading as json')
        file_mat = load('../dump_data/data_example.mat', squeeze_arrays=True)
        print('Finished loading as Matlab file')
        file_df = load('../dump_data/data_example.csv', downcast_type=True)
        print('Finished loading as csv')
        file_excel = load('../dump_data/data_example.xls', downcast_type=True)
        print('Finished loading as xls')
        file_excel2 = load('../dump_data/data_example.xlsx', downcast_type=True)
        print('Finished loading as xlsx')
        file_excel3 = load('../dump_data/data_example.ods', downcast_type=True)
        print('Finished loading as ods')

        # Error example for not supported data
        if error_invalid_type_option:
            file_error = load('../dump_data/data_example.sql')

    if reduce_function_option:
        df = load('../dump_data/Taxi_Dataset.csv')
        print('Total data frame memory '
              'before reduce [MB]: {}'.format(round(df.memory_usage(deep=True).sum() / 1024 * 1e-3, 2)))
        df = reduce_df_size(df)
        print('Total data frame memory '
              'after reduce [MB]: {}'.format(round(df.memory_usage(deep=True).sum() / 1024 * 1e-3, 2)))

        # df.to_parquet(path='../dump_data/Taxi_Dataset.parquet')
        # df = pd.read_parquet('../dump_data/Taxi_Dataset.parquet')
