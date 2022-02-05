from textwrap import wrap

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

from schemas import CourseSchema
from util import ReadingLogsData, set_plot_settings


def analyze_num_paragraphs():
    reading_logs_data = ReadingLogsData()
    adjusted_reading_speeds = []
    num_paragraphs_list = []
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not CourseSchema.page_is_valid(module_num, page_data):
                continue
            num_paragraphs_list.append(
                len(reading_logs_data.get_paragraph_list(module_num, page_num))
            )
            adjusted_reading_speeds.append(
                reading_logs_data.page_reading_speed(module_num, page_num)[1]
            )

    plot_scatter(num_paragraphs_list, adjusted_reading_speeds, 'Reading speeds as a function of page paragraph count')


def plot_scatter(x: [], y: [], title):
    set_plot_settings()
    plt.scatter(x, y)
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=80)

    plt.xlabel("Number of Paragraphs")
    plt.ylabel("Average Class Reading Speed")
    plt.title("\n".join(wrap(f"{title}")))
    plt.show()

    plt.hist2d(x, y, (50, 50), cmap=plt.cm.jet)
    plt.colorbar()
    plt.show()
