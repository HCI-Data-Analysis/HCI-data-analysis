import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from util import ReadingLogsData, PreTestData
from schemas import CourseSchema

module_content_quiz_attempt_mean = []
module_content_quiz_attempt_std = []
content_quiz_attempt_modules = []

module_content_quiz_grade_mean = []
module_content_quiz_grade_std = []
content_quiz_grade_modules = []


def content_quiz_attempts_analysis():
    r = ReadingLogsData()

    page_content_quiz_attempt_mean = []
    page_content_quiz_attempt_std = []
    content_quiz_attempt_pages = []

    # module_content_quiz_attempt_mean = []
    # module_content_quiz_attempt_std = []
    # content_quiz_attempt_modules = []

    module_paragraphs_dict = r.get_module_paragraphs_dict()
    for module_num, page_dict in module_paragraphs_dict.items():
        for page_num, page_data in page_dict.items():
            if not CourseSchema.page_is_valid(module_num, page_num):
                continue

            # set up for per page analysis
            page_attempt = r.page_content_quiz_num_attempts(module_num, page_num)
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
    page_content_quiz_attempt_std.append(np.std(page_content_quiz_attempt_mean))
    page_content_quiz_attempt_mean.append(np.mean(page_content_quiz_attempt_mean))
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
    module_content_quiz_attempt_std.append(np.std(module_content_quiz_attempt_mean))
    content_quiz_attempt_modules.append('Overall')

    plt.scatter(content_quiz_attempt_modules, module_content_quiz_attempt_mean)
    plt.errorbar(content_quiz_attempt_modules, module_content_quiz_attempt_mean, yerr=module_content_quiz_attempt_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number")
    plt.ylabel("Number of attempts")
    plt.title("Mean and Standard Deviation of Extra Attempts for Each Module")
    plt.show()


def content_quiz_grade_analysis(data448_ids):
    r = ReadingLogsData()

    page_content_quiz_grade_mean = []
    page_content_quiz_grade_std = []
    content_quiz_grade_pages = []

    content_quiz_student_average_dict = {}

    module_paragraphs_dict = r.get_module_paragraphs_dict()
    content_quiz_grade = []
    pre_test_grade = []

    for module_num, page_dict in module_paragraphs_dict.items():
        if not module_is_for_content_quiz(module_num):
            continue
        module_student_average_df = pd.DataFrame(index=data448_ids, columns=['module_average'])

        # set up for per module analysis
        module_grade = r.module_content_quiz_first_attempt_grade(module_num)
        if module_grade is not None:
            content_quiz_grade_modules.append(str(module_num))
            module_content_quiz_grade_mean.append(module_grade[0])
            module_content_quiz_grade_std.append(module_grade[1])

        for page_num, page_data in page_dict.items():
            if not page_is_for_content_quiz(module_num, page_num):
                continue

            # set up for per page analysis
            page_grade = r.page_content_quiz_first_attempt_grade(module_num=module_num, page_num=page_num)
            if page_grade is not None:
                content_quiz_grade_pages.append(str(module_num) + "-" + str(page_num))
                page_content_quiz_grade_mean.append(page_grade[0])
                page_content_quiz_grade_std.append(page_grade[1])

        # set up for individual data points
        for data448_id in data448_ids:
            module_student_average = r.module_content_quiz_first_attempt_grade(module_num, data448_id)
            if module_student_average is not None:
                module_student_average_df.loc[data448_id, 'module_average'] = module_student_average
            else:
                module_student_average_df.drop(index=data448_id)

        module_student_average_df = module_student_average_df.dropna()
        content_quiz_student_average_dict[module_num] = module_student_average_df

    p = PreTestData()
    pre_test_grade_dict = p.get_parsed_first_attempt_grades()

    for module_num, page_dict in module_paragraphs_dict.items():
        if not module_is_for_content_quiz(module_num):
            continue
        pre_test_vs_content_quiz_df = pd.DataFrame(index=data448_ids, columns=['content_quiz', 'pre_test'])
        content_quiz_df = content_quiz_student_average_dict[module_num]
        pre_test_df = pre_test_grade_dict[module_num]

        pre_test_vs_content_quiz_df['content_quiz'] = content_quiz_df['module_average']

        for data448_id in pre_test_df['data448_id']:
            student_pre_test_grade = pre_test_df[pre_test_df['data448_id'] == data448_id]['percentage'].values[0]
            pre_test_vs_content_quiz_df.loc[data448_id, 'pre_test'] = student_pre_test_grade

        dict_columns_type = {'pre_test': float, 'content_quiz': float}
        pre_test_vs_content_quiz_df = pre_test_vs_content_quiz_df.astype(dict_columns_type)

        g = sns.lmplot(x="pre_test", y="content_quiz", data=pre_test_vs_content_quiz_df)
        g.set_xlabels("Pre-test First Attempt Grade")
        g.set_ylabels("Content Quiz First Attempt Grade")
        plt.title(f'Module {module_num}')
        plt.show()

        print("Content Quiz First Attempt Grade vs Pre-Test First Attempt Grade Correlation Coefficient")
        corr_coef = np.corrcoef(x=pre_test_vs_content_quiz_df['pre_test'], y=pre_test_vs_content_quiz_df['content_quiz'])
        print(corr_coef)
        print('R^2')
        print(np.square(corr_coef))

    # Per page graph
    overall_mean = np.mean(page_content_quiz_grade_mean)
    page_content_quiz_grade_mean.append(overall_mean)
    page_content_quiz_grade_std.append(np.std(page_content_quiz_grade_mean))
    content_quiz_grade_pages.append('Overall')

    plt.scatter(content_quiz_grade_pages, page_content_quiz_grade_mean)
    plt.errorbar(content_quiz_grade_pages, page_content_quiz_grade_mean, yerr=page_content_quiz_grade_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number-Page_number")
    plt.ylabel("Number of grades")
    plt.title("Mean and Standard Deviation of First Attempt Grade for Each Content Quiz")
    plt.show()
    print("Average of first attempt content quiz grade")
    print(overall_mean)

    # Per module graph
    module_content_quiz_grade_mean.append(np.mean(module_content_quiz_grade_mean))
    module_content_quiz_grade_std.append(np.std(module_content_quiz_grade_mean))
    content_quiz_grade_modules.append('Overall')

    plt.scatter(content_quiz_grade_modules, module_content_quiz_grade_mean)
    plt.errorbar(content_quiz_grade_modules, module_content_quiz_grade_mean, yerr=module_content_quiz_grade_std,
                 fmt='o', ecolor="skyblue", elinewidth=0.5)
    plt.xticks(fontsize=5)
    plt.xlabel("Module_number")
    plt.ylabel("First attempt grades")
    plt.title("Mean and Standard Deviation of First Attempt Grade for Each Module")
    plt.show()


def module_is_for_content_quiz(module_num: int):
    if isinstance(module_num, str):
        module_num = int(module_num)

    if module_num in [0, 9, 10, 11]:
        return False

    return True


def page_is_for_content_quiz(module_num: int, page_num: int):
    if isinstance(module_num, str):
        module_num = int(module_num)
    if isinstance(page_num, str):
        page_num = int(page_num)

    if module_num in [0, 9, 10, 11]:
        return False

    if module_num in CourseSchema.OPTIONAL_PAGES and \
            page_num in CourseSchema.OPTIONAL_PAGES[module_num]:
        return False

    return True
