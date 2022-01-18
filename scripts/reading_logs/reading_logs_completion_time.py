import pandas as pd
from matplotlib import pyplot as plt
from schemas import CourseSchema
from util import ReadingLogsData


def reading_logs_completion_time(expected_reading_times):
    """
    Gets the reading logs and determines the average completion for each module. It then plots the average reading
    time vs. the expected reading time.
    :param expected_reading_times: The list of expected reading times in minutes.
    """
    average_completion = {}
    reading_logs = ReadingLogsData()
    for module in CourseSchema.MODULE_NUM_KEY.values():
        reading_duration = reading_logs.module_reading_duration(module)
        average_completion[module] = {
            'average_completion_time': reading_duration[0],
            'std': reading_duration[1]
        }
    modules_std = []
    average_completion_times = []
    for module in list(average_completion.values()):
        average_completion_times.append(module['average_completion_time'])
        modules_std.append(module['std'])
    _plot_reading_logs(list(average_completion.keys()), average_completion_times, expected_reading_times, modules_std)


def _plot_reading_logs(modules, actual_reading_times, expected_reading_times, stds):
    """
    Plots the average reading time vs. the expected reading time.
    :param modules: A list of the module numbers.
    :param actual_reading_times: A list of the reading times corresponding to the module numbers.
    :param expected_reading_times: A list of the expected reading times corresponding to the module numbers.
    :param stds: A list of the standard deviation in reading times for each module.
    """
    actual_data = {
        'Module': modules,
        'Actual Time': actual_reading_times,
        'Expected Time': expected_reading_times,
        'STD': stds
    }
    df = pd.DataFrame(actual_data)
    ax = plt.gca()
    df.plot(kind='line', x='Module', y='Actual Time', ax=ax, x_compat=True, yerr=df['STD'])
    df.plot(kind='line', x='Module', y='Expected Time', color='red', ax=ax, x_compat=True)
    plt.xticks(modules)
    plt.ylabel('Time')
    plt.show()
