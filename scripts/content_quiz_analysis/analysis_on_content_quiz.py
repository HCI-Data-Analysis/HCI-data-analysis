import matplotlib.pyplot as plt
import numpy as np
from util import ReadingLogsData
from schemas import CourseSchema


def content_quiz_attempts_analysis(content_quiz_dict):
    r = ReadingLogsData()

    page_content_quiz_attempt_mean = []
    page_content_quiz_attempt_std = []
    content_quiz_attempt_pages = []

    module_content_quiz_attempt_mean = []
    module_content_quiz_attempt_std = []
    content_quiz_attempt_modules = []

    module_paragraphs_dict = r.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not CourseSchema.page_is_valid(module_num, page_data):
                continue

            # set up for per page analysis
            page_attempt = r.page_content_quiz_num_attempts(module_num=module_num, page_num=page_num)
            if page_attempt is not None:
                content_quiz_attempt_pages.append(str(module_num)+"-"+str(page_num))
                page_content_quiz_attempt_mean.append(page_attempt[0])
                page_content_quiz_attempt_std.append(page_attempt[1])

            # set up for per module analysis
            module_attempt = r.module_content_quiz_num_attempts(module_num)
            if module_attempt is not None:
                content_quiz_attempt_modules.append(str(module_num))
                module_content_quiz_attempt_mean.append(module_attempt[0])
                module_content_quiz_attempt_std.append(module_attempt[1])

    # Per page graph
    page_content_quiz_attempt_mean.append(np.mean(page_content_quiz_attempt_mean))
    page_content_quiz_attempt_std.append(np.std(page_content_quiz_attempt_std))
    content_quiz_attempt_pages.append('Overall')

    plt.scatter(content_quiz_attempt_pages, page_content_quiz_attempt_mean)
    plt.errorbar(content_quiz_attempt_pages, page_content_quiz_attempt_mean, yerr=page_content_quiz_attempt_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("Number of attempts")
    plt.title("Mean and Standard Deviation of Extra Attempts for Each Content Quiz")
    plt.show()

    # Per module graph
    module_content_quiz_attempt_mean.append(np.mean(module_content_quiz_attempt_mean))
    module_content_quiz_attempt_std.append(np.std(module_content_quiz_attempt_std))
    content_quiz_attempt_modules.append('Overall')

    plt.scatter(content_quiz_attempt_modules, module_content_quiz_attempt_mean)
    plt.errorbar(content_quiz_attempt_modules, module_content_quiz_attempt_mean, yerr=module_content_quiz_attempt_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number")
    plt.ylabel("Number of attempts")
    plt.title("Mean and Standard Deviation of Extra Attempts for Each Module")
    plt.show()


def content_quiz_grade_analysis(content_quiz_dict):
    r = ReadingLogsData()

    page_content_quiz_grade_mean = []
    page_content_quiz_grade_std = []
    content_quiz_grade_pages = []

    module_content_quiz_grade_mean = []
    module_content_quiz_grade_std = []
    content_quiz_grade_modules = []

    module_paragraphs_dict = r.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not CourseSchema.page_is_valid(module_num, page_data):
                continue

            # set up for per page analysis
            page_grade = r.page_content_quiz_first_attempt_grade(module_num=module_num, page_num=page_num)
            if page_grade is not None:
                content_quiz_grade_pages.append(str(module_num) + "-" + str(page_num))
                page_content_quiz_grade_mean.append(page_grade[0])
                page_content_quiz_grade_std.append(page_grade[1])

            # set up for per module analysis
            module_grade = r.module_content_quiz_first_attempt_grade(module_num)
            if module_grade is not None:
                content_quiz_grade_modules.append(str(module_num))
                module_content_quiz_grade_mean.append(module_grade[0])
                module_content_quiz_grade_std.append(module_grade[1])

    # Per page graph
    page_content_quiz_grade_mean.append(np.mean(page_content_quiz_grade_mean))
    page_content_quiz_grade_std.append(np.std(page_content_quiz_grade_std))
    content_quiz_grade_pages.append('Overall')

    plt.scatter(content_quiz_grade_pages, page_content_quiz_grade_mean)
    plt.errorbar(content_quiz_grade_pages, page_content_quiz_grade_mean, yerr=page_content_quiz_grade_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("Number of grades")
    plt.title("Mean and Standard Deviation of First Attempt Grade for Each Content Quiz")
    plt.show()

    # Per module graph
    module_content_quiz_grade_mean.append(np.mean(module_content_quiz_grade_mean))
    module_content_quiz_grade_std.append(np.std(module_content_quiz_grade_std))
    content_quiz_grade_modules.append('Overall')

    plt.scatter(content_quiz_grade_modules, module_content_quiz_grade_mean)
    plt.errorbar(content_quiz_grade_modules, module_content_quiz_grade_mean, yerr=module_content_quiz_grade_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number")
    plt.ylabel("First attempt grades")
    plt.title("Mean and Standard Deviation of First Attempt Grade for Each Module")
    plt.show()
