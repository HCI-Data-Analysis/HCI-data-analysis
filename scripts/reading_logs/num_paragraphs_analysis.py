from textwrap import wrap

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

from schemas import CourseSchema
from util import ReadingLogsData, set_plot_settings
from util.reading_logs import aggregate_and_sd


def analyze_num_paragraphs():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds, v_err = [], []
    num_attempts, n_err = [], []
    num_paragraphs_list = []
    num_paragraphs_list_mod = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not CourseSchema.page_is_valid(module_num, page_num):
                continue

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
    plt.title('\n'.join(wrap('Average reading speed as a function of page paragraph count')))
    plt.xlim(0, max(num_paragraphs_list) + 2)

    plot_best_fit(num_paragraphs_list, adjusted_reading_speeds)
    linear_regression_data(num_paragraphs_list, adjusted_reading_speeds, 'Reading Speeds')
    plot_avg_reading_speed(num_paragraphs_list)
    plt.legend()
    plt.show()

    _, ax2 = plt.subplots()
    ax2.errorbar(num_paragraphs_list_mod, num_attempts, ls='none', yerr=n_err, capsize=2, elinewidth=0.4,
                 marker='.', markersize=4)
    plt.xlabel('Number of paragraphs')
    plt.ylabel('Content Quiz Attempt Number')
    plt.title('\n'.join(wrap('Content quiz attempt number as a function of page paragraph count')))
    plt.xlim(0, max(num_paragraphs_list_mod) + 2)

    plot_best_fit(num_paragraphs_list_mod, num_attempts)
    linear_regression_data(num_paragraphs_list_mod, num_attempts, 'Content Quiz Performance')
    plt.legend()
    plt.show()

    print(aggregate_and_sd(num_paragraphs_list))
    print(len(num_paragraphs_list))
    print([i for i in num_paragraphs_list if i < 2 or i > 18])
    print(len([i for i in num_paragraphs_list if i < 2 or i > 18]))

    print(aggregate_and_sd(num_paragraphs_list_mod))
    print(len(num_paragraphs_list_mod))


def plot_avg_reading_speed(x_list: []):
    x_for_line = [i for i in range(0, max(x_list) + 10)]
    y_for_line = [CourseSchema.AVERAGE_READING_SPEED for _ in x_for_line]
    plt.plot(x_for_line, y_for_line, lw=1, color='green', alpha=0.5,
             label=f'Normal Human Reading Speed ({CourseSchema.AVERAGE_READING_SPEED} WPM)')


def plot_best_fit(x_list: [], y_list: []):
    x_points = [[i] for i in x_list]
    reg = LinearRegression().fit(x_points, y_list)
    x_for_line = [i for i in range(0, max(x_list) + 10)]
    y_for_line = [reg.coef_[0] * i + reg.intercept_ for i in x_for_line]
    plt.plot(x_for_line, y_for_line, lw=1, color='red', alpha=0.5, label='Line of Best Fit')


def linear_regression_data(x_list: [], y_list: [], title: str = None) -> None:
    x_points = [[i] for i in x_list]
    reg = LinearRegression().fit(x_points, y_list)
    if title:
        print(title)
    print(f'y = {reg.coef_[0]}*x + ({reg.intercept_})\tR^2 = {reg.score(x_points, y_list)}')
