from collections import defaultdict
from textwrap import wrap

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import hsv_to_rgb
from scipy.stats import gaussian_kde

from schemas import CourseSchema
from util import ReadingLogsData, set_plot_settings


def analyze_paragraph_length_reading_speed():
    reading_logs_data = ReadingLogsData()
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    reading_duration_dict = reading_logs_data.get_reading_duration_dict()

    section_lengths = []
    reading_speeds = []

    for module_num, module_data in module_paragraphs_dict.items():
        for page_num, page_data in module_data.items():
            page_duration_df = reading_duration_dict[f'{module_num}-{page_num}']
            for section_num, section_data in page_data['sections'].items():
                # NOTE: We didn't collect paragraph specific data
                section_title = section_data['title']
                pass
    pass


def analyze_avg_paragraph_length():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds, v_err = [], []
    num_attempts, n_err = [], []
    avg_para_lengths, p_err = [], []
    avg_para_lengths_mod, p_mod_err = [], []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            p, pe = reading_logs_data.average_words_per_paragraphs_on_page(module_num, page_num)
            v, ve = reading_logs_data.page_reading_speed(module_num, page_num)
            adjusted_reading_speeds.append(v)
            v_err.append(ve)
            avg_para_lengths.append(p)
            p_err.append(pe)

            n_val = reading_logs_data.page_content_quiz_num_attempts(module_num, page_num)
            if n_val is not None:
                avg_para_lengths_mod.append(p)
                p_mod_err.append(pe)
                n, ne = n_val
                num_attempts.append(n)
                n_err.append(ne)

    set_plot_settings()
    _, ax = plt.subplots()
    ax.errorbar(avg_para_lengths, adjusted_reading_speeds, ls='none', xerr=p_err, yerr=v_err, capsize=2, elinewidth=0.4,
                marker='.', markersize=4)
    plt.xlabel('Average Page Paragraph Length')
    plt.ylabel('Average reading speed (WPM)')
    plt.title('\n'.join(wrap('Average reading speed as a function of the number of paragraphs on a page')))

    _, ax2 = plt.subplots()
    ax2.errorbar(avg_para_lengths_mod, num_attempts, ls='none', xerr=p_mod_err, yerr=n_err, capsize=2, elinewidth=0.4,
                 marker='.', markersize=4)
    plt.xlabel('Average Page Paragraph Length')
    plt.ylabel('Content Quiz Attempt Number')
    plt.title('\n'.join(wrap('Content quiz attempt number as a function of the number of paragraphs on a page')))

    plt.show()


def analyze_num_paragraphs():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds, v_err = [], []
    num_attempts, n_err = [], []
    num_paragraphs_list = []
    num_paragraphs_list_mod = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            num_paragraphs = len(reading_logs_data.get_paragraph_list(module_num, page_num))

            num_paragraphs_list.append(num_paragraphs)
            v, ve = reading_logs_data.page_reading_speed(module_num, page_num)
            adjusted_reading_speeds.append(v)
            v_err.append(ve)

            n_val = reading_logs_data.page_content_quiz_num_attempts(module_num, page_num)
            if n_val is not None:
                n, ne = n_val
                num_paragraphs_list_mod.append(num_paragraphs)
                num_attempts.append(n)
                n_err.append(ne)

    set_plot_settings()
    _, ax = plt.subplots()
    ax.errorbar(num_paragraphs_list, adjusted_reading_speeds, ls='none', yerr=v_err, capsize=2, elinewidth=0.4,
                marker='.', markersize=4)
    plt.xlabel('Number of paragraphs')
    plt.ylabel('Average reading speed (WPM)')
    plt.title('\n'.join(wrap('Average reading speed as a function of the number of paragraphs on a page')))

    _, ax2 = plt.subplots()
    ax2.errorbar(num_paragraphs_list_mod, num_attempts, ls='none', yerr=n_err, capsize=2, elinewidth=0.4,
                 marker='.', markersize=4)
    plt.xlabel('Number of paragraphs')
    plt.ylabel('Content Quiz Attempt Number')
    plt.title('\n'.join(wrap('Content quiz attempt number as a function of the number of paragraphs on a page')))

    plt.show()


def analyze_num_paragraphs_reading_speed():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds = []
    adjusted_reading_speeds_error = []
    average_words_in_paras = []
    average_words_in_paras_error = []
    num_paragraphs_list = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            # if not page_is_valid(module_num, page_data):
            #     continue
            adjusted_reading_speed, error = reading_logs_data.page_reading_speed(
                module_num,
                page_num
            )
            average_words_in_para, average_words_in_para_error = reading_logs_data.average_words_per_paragraphs_on_page(
                module_num,
                page_num
            )

            if average_words_in_para:
                num_paragraphs_list.append(
                    len(reading_logs_data.get_paragraph_list(module_num, page_num))
                )
                adjusted_reading_speeds.append(adjusted_reading_speed)
                adjusted_reading_speeds_error.append(error)
                average_words_in_paras.append(average_words_in_para)
                average_words_in_paras_error.append(average_words_in_para_error)

    for i in range(1, 3):
        plot_scatter(
            average_words_in_paras,
            adjusted_reading_speeds,
            num_paragraphs_list,
            'Reading speeds as a function of average page paragraph length',
            i,
            'Average Reading Speed (WPM)',
            average_words_in_paras_error,
            adjusted_reading_speeds_error
        )
    counts(num_paragraphs_list, average_words_in_paras)


def analyze_num_paragraphs_content_quiz():
    reading_logs_data = ReadingLogsData()
    average_words_in_paras = []
    average_words_in_paras_error = []
    num_paragraphs_list = []
    num_attempts_neeeded = []
    num_attempts_neeeded_error = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            # if not page_is_valid(module_num, page_data):
            #     continue
            average_words_in_para, average_words_in_para_error = reading_logs_data.average_words_per_paragraphs_on_page(
                module_num,
                page_num
            )

            num_attempts_data = reading_logs_data.page_content_quiz_num_attempts(
                module_num,
                page_num
            )

            # Note: Excludes when data doesn't exist (no quiz or no words)
            if average_words_in_para and num_attempts_data:
                average_num_attempts, average_num_attempts_error = num_attempts_data
                num_paragraphs_list.append(
                    len(reading_logs_data.get_paragraph_list(module_num, page_num))
                )
                average_words_in_paras.append(average_words_in_para)
                average_words_in_paras_error.append(average_words_in_para_error)
                num_attempts_neeeded.append(average_num_attempts)
                num_attempts_neeeded_error.append(average_num_attempts_error)

    for i in range(1, 3):
        plot_scatter(
            average_words_in_paras,
            num_attempts_neeeded,
            num_paragraphs_list,
            'Content quiz attempt number needed as a function of average page paragraph length',
            i,
            'Content Quiz Attempt Number',
            average_words_in_paras_error,
            num_attempts_neeeded_error
        )
    counts(num_paragraphs_list, average_words_in_paras)


def page_is_valid(module_num, page_content) -> bool:
    if page_content['name'] in CourseSchema.OPTIONAL_PAGE_TITLES or module_num in CourseSchema.OPTIONAL_MODULES:
        return False
    return True


def counts(num_paragraphs_list, num_words):
    print('Min, Max Num Paragraphs')
    print(min(num_paragraphs_list), max(num_paragraphs_list))

    freq = defaultdict(int)
    for n in num_words:
        freq[round(n)] += 1

    print('Min, Max Num Paragraphs Frequency')
    print(min(freq.values()), max(freq.values()))


def plot_scatter(x: [], y: [], num_paragraphs_list: [], title, version: int, y_label: str, x_err: [] = None,
                 y_err: [] = None):
    set_plot_settings()
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    def r(i, l):
        val = (float(i) - min(l)) / (max(l) - min(l))
        hsv = (0.18 - val * 0.18, 1, 1)  # for speed
        return hsv_to_rgb(hsv)

    def b(i, l):
        val = (float(i) - min(l)) / (max(l) - min(l))
        # hsv = (0.15 - val * 0.15, 1, 1)  # for speed
        hsv = (0.65 - val * 0.18, 1, 1)
        return hsv_to_rgb(hsv)

    norm = [r(i, num_paragraphs_list) for i in num_paragraphs_list]
    norm_z = [b(i, z) for i in z]

    fig, ax = plt.subplots()

    for xi, yi, xe, ye, c in zip(x, y, x_err, y_err, norm):
        if version == 1:
            ax.errorbar(xi, yi, xerr=xe, yerr=ye, capsize=2, elinewidth=0.4, c=c, marker='.', markersize=4)
        if version == 2:
            ax.errorbar(xi, yi, elinewidth=0.4, c=c, marker='.')

    for xi, yi, xe, ye, c in zip(x, y, x_err, y_err, norm_z):
        if version == 3:
            ax.errorbar(xi, yi, elinewidth=0.4, c=c, marker='.')
        if version == 4:
            ax.errorbar(xi, yi, xerr=xe, yerr=ye, capsize=2, elinewidth=0.4, c=c, marker='.', markersize=4)

    plt.xlabel('Average Page Paragraph Length')
    # plt.ylabel('Average Class Reading Speed')  # for speed
    plt.ylabel(y_label)  # for speed
    # plt.ylabel('Average Number of Content Quiz Attempts before correct')
    plt.title('\n'.join(wrap(f'{title}')))
    plt.show()
