from abc import ABCMeta
from pathlib import Path
from os.path import isfile
from datetime import datetime

from personal_tools.in_out import get_or_create_folder


# Work in both Pycharm and terminal
actual_path = Path().absolute()
project_path = None
# Tries to find the project path based on a setup.py file
# TODO: Needs to improve this logic
while not actual_path.absolute() == actual_path.cwd().drive:
    if isfile(actual_path / 'setup.py') or isfile(actual_path / 'requirements.txt'):
        project_path = actual_path
        break
    actual_path = actual_path.parent

if project_path is None:
    raise IOError('Could not find project folder')


# Project folder structure
class FolderStructure(ABCMeta):
    PROJECT_PATH = actual_path
    CONFIGURATIONS_PATH = PROJECT_PATH / 'configurations'
    SCRIPTS_PATH = PROJECT_PATH / 'scripts'
    RESULTS = get_or_create_folder(PROJECT_PATH / 'results')
    FIGURES = RESULTS / 'Figures'

    @classmethod
    def set_results_path(cls, path_name: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                         complete_path: bool = False):
        cls.reset_results()
        if not complete_path:
            cls.add_sub_folder(path_name)
        else:
            cls.RESULTS = Path(path_name)
        cls.FIGURES = get_or_create_folder(cls.RESULTS / 'Figures')

    @classmethod
    def add_sub_folder(cls, name):
        cls.RESULTS = get_or_create_folder(cls.RESULTS / '{}'.format(name))

    @classmethod
    def reset_results(cls):
        cls.RESULTS = get_or_create_folder(cls.PROJECT_PATH / 'results')

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
        return cls.RESULTS

    @classmethod
    def fig_path(cls) -> Path:
        return get_or_create_folder(cls.FIGURES)


