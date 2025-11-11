"""
Module containing functions for input and output of data, and for folder creation and paths.
"""
from pathlib import Path
from os.path import exists, isfile
from os import makedirs, chmod, path, walk
from pprint import pformat
from pandas import read_csv, DataFrame, read_excel, ExcelWriter
from numpy import squeeze, ndarray, load as load_np, save as save_np, random
from json import load as load_json, dump as save_json
from scipy.io import loadmat as load_mat, savemat as save_mat
from shutil import rmtree
from stat import S_IRWXU, S_IRWXG, S_IRWXO
from zipfile import ZipFile, ZIP_DEFLATED
from pickle import dump as save_pickle, load as load_pickle

from research_tools.utils import update_default_dict, squeeze_dict, Union, Dict, format_dict_json, reduce_df_size
from research_tools.error_handling import handleRemoveReadonly

SAVE_DEFAULT_CSV_PARAMS = {'index': False, }
SAVE_DEFAULT_JSON_PARAMS = {'indent': 2, }
SAVE_DEFAULT_PRETTY_PRINT_JSON_PARAMS = {'indent': 2, 'width': 120, 'compact': True, 'sort_dicts': False, }
SAVE_DEFAULT_NPY_PARAMS = {}
SAVE_DEFAULT_MAT_PARAMS = {}
SAVE_DEFAULT_EXCEL_PARAMS = {'header': True, 'index': False, }
LOAD_DEFAULT_EXCEL_PARAMS = {'sheet_name': None, }
PRETTY_PRINT_OPTION = True


def load(file_path: Union[Path, str], squeeze_arrays: bool = True, remove_matlab_keys: bool = True,
         downcast_type: bool = False, **kwargs) -> Union[dict, Dict[str, DataFrame], DataFrame, ndarray, str]:
    """
    Load main types of data used in our work.
    Working with the following extensions: .json, .csv, .mat, .npy, .npz, .xlsx, .xls, .ods, .txt, and .pickle.

    :param file_path: File path
    :param squeeze_arrays: Option to squeeze arrays within the dict (Used for numpy array and .mat files)
    :param remove_matlab_keys: Option to remove the Matlab parameters from the dict (Used for .mat files).
    True if the data should remove the Matlab information.
    :param downcast_type: Option to apply a downcast function to the data (Used for .csv and Excel files)
    :param kwargs: Parameters of the respective load function
    :return: Data loaded
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if file_path.suffix in ['.json']:
        with open(file_path, 'r') as file:
            data = load_json(file, **kwargs)
            for key, value in data.items():
                if value == 'true':
                    data[key] = True
                elif value == 'false':
                    data[key] = False
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
        data = read_excel(io=file_path, **update_default_dict(LOAD_DEFAULT_EXCEL_PARAMS, kwargs))
        if len(data.keys()) == 0:
            raise ValueError('Excel file does not present any dataframe.')
        if len(data.keys()) == 1:
            data = data[list(data.keys())[0]]
            if downcast_type:
                data = reduce_df_size(data)
        elif len(data.keys()) > 1 and downcast_type:
            for key, data_frame in data.items():
                data[key] = reduce_df_size(data_frame)
    elif file_path.suffix in ['.txt']:
        with open(file_path, 'r') as file:
            data = file.read()
    elif file_path.suffix in ['.pickle']:
        with open(file_path, 'rb') as file:
            data = load_pickle(file)
    else:
        raise TypeError('Load function not implemented for "{}" type'.format(file_path.suffix))

    return data


def save(file_path: Union[Path, str], data: Union[dict, DataFrame, ndarray, str],
         json_pretty_print: bool = PRETTY_PRINT_OPTION, **kwargs):
    """
    Save the main types of data used in our work.
    Using the default parameters of the respective save function, unless set different.
    Working with the following extensions: .json, .csv, .mat, .npy, .npz, .xlsx, .xls, .ods, .txt, and .pickle.

    :param file_path: File path
    :param data: Data to save
    :param json_pretty_print: Use the pretty print library to produce the json file
    :param kwargs: Parameters of the respective save function
    :return:
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if file_path.suffix in ['.json']:
        data = format_dict_json(data)
        with open(file_path, 'w') as file:
            if not json_pretty_print:
                save_json(obj=data, fp=file, **update_default_dict(SAVE_DEFAULT_JSON_PARAMS, kwargs))
            else:
                data_str = pformat(data, **update_default_dict(SAVE_DEFAULT_PRETTY_PRINT_JSON_PARAMS, kwargs))
                # Replace ' and None symbols
                data_str = data_str.replace("'", '"')
                data_str = data_str.replace(' None', ' null')
                data_str = data_str.replace(' True', ' true')
                data_str = data_str.replace(' False', ' false')
                file.write(data_str)
    elif file_path.suffix in ['.csv']:
        data.to_csv(path_or_buf=file_path, **update_default_dict(SAVE_DEFAULT_CSV_PARAMS, kwargs))
    elif file_path.suffix in ['.mat']:
        save_mat(file_name=file_path, mdict=data, **update_default_dict(SAVE_DEFAULT_MAT_PARAMS, kwargs))
    elif file_path.suffix in ['.npy', '.npz']:
        save_np(file=file_path, arr=data, **update_default_dict(SAVE_DEFAULT_NPY_PARAMS, kwargs))
    elif file_path.suffix in ['.xlsx', '.xls', '.ods']:
        if isinstance(data, DataFrame):
            data.to_excel(excel_writer=file_path, **update_default_dict(SAVE_DEFAULT_EXCEL_PARAMS, kwargs))
        elif isinstance(data, dict):
            with ExcelWriter(file_path, engine='openpyxl') as writer:
                for sheet_name, dataframe in data.items():
                    dataframe.to_excel(writer, sheet_name=sheet_name,
                                       **update_default_dict(SAVE_DEFAULT_EXCEL_PARAMS, kwargs))
    elif file_path.suffix in ['.txt']:
        with open(file_path, 'w') as file:
            file.write(data)
    elif file_path.suffix in ['.pickle']:
        with open(file_path, 'wb') as file:
            # noinspection PyTypeChecker
            save_pickle(obj=data, file=file)
    else:
        raise TypeError('Save function not implemented for "{}" type'.format(file_path.suffix))


def get_or_create_folder(folder_path: Union[Path, str]) -> Path:
    """
    Creates entire folder path if it does not exist.

    :param folder_path: Folder path
    :return: Same folder path, but with created folder if it does not exist
    """
    folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path

    if not exists(folder_path):
        makedirs(folder_path)

    return folder_path


def remove_file_or_folder_and_content(file_path: Union[Path, str], force: bool = False) -> None:
    """
    Delete a file or a folder and its content, possibly forcing the deletion.

    :param file_path: File or folder path.
    :param force: Option to force the deletion if the error is related to access .
    :return:
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path

    if file_path.is_file():
        if force:
            chmod(file_path, S_IRWXU | S_IRWXG | S_IRWXO)
        file_path.unlink()
    elif file_path.is_dir():
        if force:
            rmtree(file_path, ignore_errors=False, onerror=handleRemoveReadonly)
        else:
            rmtree(file_path, ignore_errors=False)
    else:
        raise ValueError('Invalid type to delete. Not folder or file')


def zip_folder_and_content(folder_path: Union[Path, str], name: str = None, delete_folder: bool = False):
    """
    Function to zip the folder and its content.

    :param folder_path: Folder path
    :param name: Name of the zip file (String to be attached at the folder path)
    :param delete_folder: Option to delete the folder after zip
    :return:
    """
    folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path
    name = folder_path.stem if name is None else name

    with ZipFile(folder_path.parent / f'{name}.zip', 'w', ZIP_DEFLATED) as zip_file:
        for root, dirs, files in walk(folder_path):
            for file in files:
                file_path = path.join(root, file)
                arc_name = path.relpath(file_path, folder_path)
                zip_file.write(file_path, arc_name)

    if delete_folder:
        remove_file_or_folder_and_content(folder_path, force=True)


def extract_to_folder(file_path: Union[Path, str], folder_name: str = None, output_path: Union[str, Path] = None,
                      delete_file: bool = False):
    """
    Function to extract a zip file to a folder.

    :param file_path: Path to the file
    :param folder_name: New folder name (Optional)
    :param output_path: Output path (Optional)
    :param delete_file: Option to delete the extracted file
    :return:
    """
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    output_path = Path(output_path) if isinstance(output_path, str) else output_path
    folder_name = file_path.stem if folder_name is None else folder_name
    output_path = file_path.parent if output_path is None else output_path
    output_path = get_or_create_folder(output_path) if not output_path.is_dir() else output_path

    with ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(path=output_path / folder_name)
    if delete_file:
        file_path.unlink()


def create_new_json(file_path: Union[Path, str], num_entrances: int = 2):
    """
    Create a generic .json file with a fixed values of entrance.

    :param file_path: File path
    :param num_entrances: Number of entrances to create
    :return:
    """
    new_dict = {f'key_{index}': f'value_{index}' for index in range(1, num_entrances + 1)}
    save(file_path=file_path, data=new_dict, json_pretty_print=False)


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
