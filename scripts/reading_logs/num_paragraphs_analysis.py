from textwrap import wrap

from matplotlib import pyplot as plt

from schemas import CourseSchema
from util import get_module_paragraphs_dict, get_average_adjusted_reading_speed, get_page_num_paragraphs, set_plot_settings


def analyze_num_paragraphs():
    adjusted_reading_speeds = []
    num_paragraphs_list = []
    module_paragraphs_dict = get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_content in page_dict.items():
            if not page_is_valid(module_num, page_content):
                continue
            num_paragraphs_list.append(get_page_num_paragraphs(page_content['paragraphs']))
            adjusted_reading_speeds.append(
                get_average_adjusted_reading_speed(module_num, page_num)
            )

    plot_scatter(num_paragraphs_list, adjusted_reading_speeds, 'Adjusted reading speeds by page paragraph count')


def page_is_valid(module_num, page_content) -> bool:
    if page_content['title'] in CourseSchema.OPTIONAL_PAGE_TITLES or module_num in CourseSchema.OPTIONAL_MODULES:
        return False
    return True


def plot_scatter(x: [], y: [], title):
    set_plot_settings()
    plt.scatter(x, y)
    plt.xlabel("Number of Paragraphs")
    plt.ylabel("Adjusted Reading Speed")
    plt.title("\n".join(wrap(f"{title}")))
    plt.show()
