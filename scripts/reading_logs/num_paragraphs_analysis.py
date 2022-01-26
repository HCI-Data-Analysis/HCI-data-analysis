import random
from textwrap import wrap

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

from schemas import CourseSchema
from util import ReadingLogsData, set_plot_settings


def analyze_num_paragraphs():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds = []
    adjusted_reading_speeds_error = []
    average_words_in_paras = []
    average_words_in_paras_error = []
    num_paragraphs_list = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not page_is_valid(module_num, page_data):
                continue
            num_paragraphs_list.append(
                len(reading_logs_data.get_paragraph_list(module_num, page_num))
            )
            adjusted_reading_speed, error = reading_logs_data.page_reading_speed(
                module_num,
                page_num
            )
            average_words_in_para, average_words_in_para_error = reading_logs_data.average_words_per_paragraphs_on_page(
                module_num,
                page_num
            )
            adjusted_reading_speeds.append(adjusted_reading_speed)
            adjusted_reading_speeds_error.append(error)

            if average_words_in_para:
                average_words_in_paras.append(average_words_in_para)
                average_words_in_paras_error.append(average_words_in_para_error)

    plot_scatter(
        average_words_in_paras,
        adjusted_reading_speeds,
        num_paragraphs_list,
        'Reading speeds as a function of page paragraph count',
        average_words_in_paras_error,
        adjusted_reading_speeds_error
    )


def page_is_valid(module_num, page_content) -> bool:
    if page_content['name'] in CourseSchema.OPTIONAL_PAGE_TITLES or module_num in CourseSchema.OPTIONAL_MODULES:
        return False
    return True


def plot_scatter(x: [], y: [], num_paragraphs_list: [], title, x_err: [] = None, y_err: [] = None):
    set_plot_settings()
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    plt.scatter(x, y, c=z)
    fig, ax = plt.subplots()

    def f(i, l):
        val = float(i) / max(l)
        return val, val, val

    norm = [f(i, num_paragraphs_list) for i in num_paragraphs_list]

    for xi, yi, xe, ye, c in zip(x, y, x_err, y_err, norm):
        ax.errorbar(xi, yi, xerr=xe, yerr=ye, fmt='o', elinewidth=0.5, c=c)

    plt.xlabel('Number of Paragraphs')
    plt.ylabel('Average Class Reading Speed')
    plt.title('\n'.join(wrap(f'{title}')))
    plt.show()