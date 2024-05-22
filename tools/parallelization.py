"""
Module responsible to manage CPU cores parallelization
"""
from abc import ABC
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

from tools.utils import Union


class CpuParallel(ABC):
    _NUM_CORES = cpu_count()

    @classmethod
    def set_num_cores(cls, num_cores: int):
        """
        Set the number of CPU cores to run the function parallelized

        :param num_cores: Number of CPU cores
        :return: None
        """
        # Validation of inserted value
        if isinstance(num_cores, float):
            if round(num_cores) == 0:
                new_num_cores = 1
            else:
                new_num_cores = round(num_cores)
            print('Number of CPU cores inserted ({}) was rounded to {}'.format(new_num_cores, num_cores))
            num_cores = new_num_cores
        elif not isinstance(num_cores, int):
            raise TypeError('Invalid type for number of CPU cores')

        # Check maximum number of CPU cores possible
        if num_cores > cpu_count():
            print('Number of CPU cores is larger than the total number of the machine\n'
                  'Using all CPU cores: {}'.format(cpu_count()))
        else:
            cls._NUM_CORES = num_cores

    @classmethod
    def get_num_cores(cls) -> int:
        return cls._NUM_CORES

    @classmethod
    def run_parallelization(cls, function, args: Union[tuple, list]) -> list:
        """
        Run a specified function, together with its arguments, in parallel.
        If an exception occur in one or more processes, print the error message(s).

        :param function: Function to run.
        :param args: List of arguments for each process.
        :return: List of results returned by the function.
        """
        with ProcessPoolExecutor(max_workers=cls._NUM_CORES) as executor:
            future_list, results = [], []
            for arg in args:
                if isinstance(arg, dict):
                    future = executor.submit(function, **arg)
                elif isinstance(arg, tuple):
                    future = executor.submit(function, arg)
                future_list.append(future)

        # Catch the exceptions, print them, and return only the results which finished successfully.
        # TODO: Decide if the result should be removed when the function returns an error (as it is) or
        #  return None (maintaining the same size)
        for future in future_list:
            try:
                results.append(future.result())
            except Exception as error_msg:
                print(error_msg)

        return results


if __name__ == '__main__':
    from tools.dump_functions import random_generation_wait_arg, random_generation_wait_param

    low_value = 2
    high_value = 5.1
    number_cores = 2
    number_times = 4

    CpuParallel.set_num_cores(number_cores)
    print('Number of CPU cores: {}'.format(CpuParallel.get_num_cores()))
    print('Number of epochs per function: {}'.format(number_times))

    args_tuple_arg = tuple((low_value, high_value) for _ in range(number_times))
    args_list_arg = list((low_value, high_value) for _ in range(number_times))
    args_list_param = list({'high': high_value, 'low': low_value} for _ in range(number_times))

    print('Running functions with arg as input for tuple of arguments')
    results_tuple_arg = CpuParallel.run_parallelization(function=random_generation_wait_arg, args=args_tuple_arg)
    print('Running functions with arg as input for list of arguments')
    results_list_arg = CpuParallel.run_parallelization(function=random_generation_wait_arg, args=args_list_arg)
    print('Running functions with dict of parameters as input for list of arguments')
    results_list_param = CpuParallel.run_parallelization(function=random_generation_wait_param, args=args_list_param)

    print('Results tuple (arg function): {}'.format(results_tuple_arg))
    print('Results list (arg function): {}'.format(results_list_arg))
    print('Results list (param function): {}'.format(results_list_param))
