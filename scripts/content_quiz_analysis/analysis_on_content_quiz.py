import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from util import ReadingLogsData


def content_quiz_analysis(content_quiz_dict):
    r = ReadingLogsData()
    content_quiz_attempt_mean = []
    content_quiz_attempt_std = []
    content_quiz_attempt_pages = []

    for page in content_quiz_dict.keys():
        split_key = page.split('-')
        module_num = split_key[0]
        page_num = split_key[1]
        page_attempt = r.page_content_quiz_num_attempts(module_num=module_num, page_num=page_num)
        if page_attempt is not None:
            page_attempt_mean = page_attempt[0]
            page_attempt_std = page_attempt[1]
            content_quiz_attempt_pages.append(page)
            content_quiz_attempt_mean.append(page_attempt_mean)
            content_quiz_attempt_std.append(page_attempt_std)

    content_quiz_attempt_mean.append(np.mean(content_quiz_attempt_mean))
    content_quiz_attempt_std.append(np.std(content_quiz_attempt_std))
    content_quiz_attempt_pages.append('Overall')

    print(content_quiz_attempt_std)

    plt.scatter(content_quiz_attempt_pages, content_quiz_attempt_mean)
    plt.errorbar(content_quiz_attempt_pages, content_quiz_attempt_mean, yerr=content_quiz_attempt_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("Number of attempts")
    plt.title("Mean and Standard Deviation of Content Quiz Attempts for Each Page")
    plt.show()



