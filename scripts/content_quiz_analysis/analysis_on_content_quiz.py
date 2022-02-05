import matplotlib.pyplot as plt
import numpy as np
from util import ReadingLogsData


def content_quiz_attempts_analysis(content_quiz_dict):
    r = ReadingLogsData()
    content_quiz_attempt_mean = []
    content_quiz_attempt_std = []
    content_quiz_attempt_pages = []

    # module_paragraphs_dict = r.get_module_paragraphs_dict()
    # for module_num, page_dict in module_paragraphs_dict.items():
    #     for page_num, page_data in page_dict.items():
    #         if not page_is_valid(module_num, page_data):
    #             continue

    for page in content_quiz_dict.keys():
        split_key = page.split('-')
        module_num = split_key[0]
        page_num = split_key[1]
        page_attempt = r.page_content_quiz_num_attempts(module_num=module_num, page_num=page_num)

        module_attempt = r.module_content_quiz_first_attempt_grade(module_num=module_num)
        #TODO: loop through each module

        if page_attempt is not None:
            page_attempt_mean = page_attempt[0]
            page_attempt_std = page_attempt[1]
            content_quiz_attempt_pages.append(page)
            content_quiz_attempt_mean.append(page_attempt_mean)
            content_quiz_attempt_std.append(page_attempt_std)

    content_quiz_attempt_mean.append(np.mean(content_quiz_attempt_mean))
    content_quiz_attempt_std.append(np.std(content_quiz_attempt_std))
    content_quiz_attempt_pages.append('Overall')

    plt.scatter(content_quiz_attempt_pages, content_quiz_attempt_mean)
    plt.errorbar(content_quiz_attempt_pages, content_quiz_attempt_mean, yerr=content_quiz_attempt_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("Number of attempts")
    plt.title("Mean and Standard Deviation of Extra Attempts for Each Content Quiz")
    plt.show()


def content_quiz_grade_analysis(content_quiz_dict):
    r = ReadingLogsData()

    content_quiz_grade_mean = []
    content_quiz_grade_std = []
    content_quiz_grade_pages = []

    for page in content_quiz_dict.keys():
        split_key = page.split('-')
        module_num = split_key[0]
        page_num = split_key[1]
        page_grade = r.page_content_quiz_first_attempt_grade(module_num=module_num, page_num=page_num)

        if page_grade is not None:
            page_grade_mean = page_grade[0]
            page_grade_std = page_grade[1]
            content_quiz_grade_pages.append(page)
            content_quiz_grade_mean.append(page_grade_mean)
            content_quiz_grade_std.append(page_grade_std)

    content_quiz_grade_mean.append(np.mean(content_quiz_grade_mean))
    content_quiz_grade_std.append(np.std(content_quiz_grade_std))
    content_quiz_grade_pages.append('Overall')

    plt.scatter(content_quiz_grade_pages, content_quiz_grade_mean)
    plt.errorbar(content_quiz_grade_pages, content_quiz_grade_mean, yerr=content_quiz_grade_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("First attempt average grade")
    plt.title("Mean and Standard Deviation of First Attempt Grade for Each Content Quiz")
    plt.show()





