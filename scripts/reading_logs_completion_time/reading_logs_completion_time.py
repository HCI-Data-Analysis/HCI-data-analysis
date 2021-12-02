import json
import pandas as pd
from pathlib import Path
from statistics import mean
from matplotlib import pyplot as plt

from schemas import ReadingLogsSchema


def reading_logs_completion_time(directory, expected_reading_times):
    """
    Gets the reading logs and determines the average completion for each module. It then plots the average reading
    time vs. the expected reading time.
    :param directory: The directory where reading logs are stored.
    :param expected_reading_times: The list of expected reading times in minutes.
    """
    average_completion = {}
    entries = Path(directory)
    for entry in entries.iterdir():
        if entry.is_dir():
            completion_times = []
            for student in Path(entry).iterdir():
                completion_times.append(_calculate_completion_time(student))
            average_completion[_get_module_name(entry.name)] = (mean(completion_times) / (1000 * 60)) % 60
    average_completion = _sort_dict_by_key(average_completion)
    _plot_reading_logs(list(average_completion.keys()), list(average_completion.values()), expected_reading_times)


def _plot_reading_logs(modules, actual_reading_times, expected_reading_times):
    """
    Plots the average reading time vs. the expected reading time.
    :param modules: A list of the module numbers.
    :param actual_reading_times: A list of the reading times corresponding to the module numbers.
    :param expected_reading_times: A list of the expected reading times corresponding to the module numbers.
    """
    actual_data = {
        'Module': modules,
        'Actual Time': actual_reading_times,
        'Expected Time': expected_reading_times
    }
    df = pd.DataFrame(actual_data)
    ax = plt.gca()
    df.plot(kind='line', x='Module', y='Actual Time', ax=ax, x_compat=True, yerr=df['Actual Time'].std())
    df.plot(kind='line', x='Module', y='Expected Time', color='red', ax=ax, x_compat=True, yerr=df['Expected Time'].std())
    plt.xticks(modules)
    plt.ylabel('Time')
    plt.show()


def _calculate_completion_time(directory):
    """
    Calculates the average completion time for a student.
    :param directory: The directory where the student's reading logs exist.
    :return: The total time it took the student to complete reading the module.
    """
    files = Path(directory).glob('*.txt')
    completion_times = []
    for file in files:
        with open(file) as f:
            try:
                contents = json.loads(f.read())
                completion_times.append(contents['endTime'] - contents['startTime'])
            except:
                print(f'{file} has an issue.')
                continue
    return sum(completion_times)


def _get_module_name(module):
    """
    Gets the module name.
    :param module: The module to get the name for.
    :return: The correct name based on the assignment number.
    """
    return ReadingLogsSchema.MODULE_NAMES.get(module)


def _sort_dict_by_key(dictionary):
    """
    The reading logs on the shared drive are sorted numerically by assignment id. This is not the same order of the
    modules, this function ensures that the dict is sorted in order of the modules instead of assignment id.
    :param dictionary: The dictionary to sort by keys.
    :return: The sorted dictionary.
    """
    sorted_items = sorted(dictionary.items())
    return dict(sorted_items)
