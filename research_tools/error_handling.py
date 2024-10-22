from errno import EACCES
from stat import S_IRWXU, S_IRWXG, S_IRWXO
from os import rmdir, remove, chmod


def handleRemoveReadonly(func, path, exc):
    """
    Handle the remove folder and content error in Windows OS, if the error is related to read-only state.

    :param func:
    :param path:
    :param exc:
    :return:
    """
    excvalue = exc[1]
    if func in (rmdir, remove) and excvalue.errno == EACCES:
        chmod(path, S_IRWXU | S_IRWXG | S_IRWXO)  # 0777
        func(path)
    else:
        raise
