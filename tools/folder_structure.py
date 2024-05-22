from abc import ABCMeta
from pathlib import Path
from os.path import isfile
from datetime import datetime

from tools.in_out import get_or_create_folder


# Work in both Pycharm and terminal
project_path = Path().absolute()

# Tries to find the project path based on a setup.py file
# TODO: Needs to improve this logic
while not project_path.absolute() == project_path.cwd().drive:
    # Project depends on having a 'setup.py' or 'requirements.txt' file in order to work
    if isfile(project_path / 'setup.py') or isfile(project_path / 'requirements.txt'):
        break
    project_path = project_path.parent

if project_path is None:
    raise IOError('Could not find project folder')


# Project folder structure
class FolderStructure(ABCMeta):
    PROJECT_PATH = project_path
    CONFIGURATIONS_PATH = PROJECT_PATH / 'configurations'
    SCRIPTS_PATH = PROJECT_PATH / 'scripts'
    RESULTS = PROJECT_PATH / 'results'
    FIGURES = RESULTS / 'Figures'

    @classmethod
    def set_results_path(cls, path_name: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                         is_complete_path: bool = False):
        """
        Function to set a folder name inside the project results folder or set a complete path for the results.
        Figures folder will be putted inside the results' folder.

        :param path_name: Name of the folder where the results will be saved.
        :param is_complete_path: Boolean to indicate if the path is complete or not.
        :return:
        """
        cls.reset_results()
        if not is_complete_path:
            cls.add_results_sub_folder(path_name)
        else:
            cls.RESULTS = Path(path_name)
        cls.FIGURES = cls.RESULTS / 'Figures'

    @classmethod
    def add_results_sub_folder(cls, name):
        cls.RESULTS = cls.RESULTS / '{}'.format(name)
        cls.FIGURES = cls.RESULTS / 'Figures'

    @classmethod
    def reset_results(cls):
        cls.RESULTS = cls.PROJECT_PATH / 'results'

    @classmethod
    def project_path(cls) -> Path:
        return cls.PROJECT_PATH

    @classmethod
    def configurations_path(cls) -> Path:
        return cls.CONFIGURATIONS_PATH

    @classmethod
    def scripts_path(cls) -> Path:
        return cls.SCRIPTS_PATH

    @classmethod
    def results_path(cls) -> Path:
        return get_or_create_folder(cls.RESULTS)

    @classmethod
    def fig_path(cls) -> Path:
        return get_or_create_folder(cls.FIGURES)


