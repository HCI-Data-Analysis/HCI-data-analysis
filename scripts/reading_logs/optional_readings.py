import re
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

from schemas import CourseSchema
from scripts import prepare_data_for_clustering
from util import ReadingLogsData
from util.reading_logs import aggregate_and_sd

LIKERT_ANSWERS = [
    'Strongly Agree',
    'Agree',
    'Disagree',
    'Strongly Disagree',
    'No Response'
]

RELEVANT_QUESTIONS = [
    'I think design and interaction is interesting.',
    'I think design and interaction is boring.',
    'I like to use design and interaction to solve problems.',
]

"""
T-Test Plan

- Explain comparison and motivation
- Histogram observe
- Note not obvious from histograms so use tests
- Difference is non normal (outliers don't conceptually make sense with opinions)
- Switch to Wilcoxon
- Wilcoxon says reject null, means are equal
- 
"""

"""
References:
https://statistics.laerd.com/statistical-guides/dependent-t-test-statistical-guide-2.php
https://statistics.laerd.com/spss-tutorials/dependent-t-test-using-spss-statistics.php
https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test
https://statistics.laerd.com/spss-tutorials/wilcoxon-signed-rank-test-using-spss-statistics.php
https://www.jstor.org/stable/3001968?seq=1#metadata_info_tab_contents
https://www.investopedia.com/terms/t/t-test.asp
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
"""


def get_cleaned_interest_data(first_survey: pd.DataFrame, second_survey: pd.DataFrame, survey_schema: pd.DataFrame):
    first_df_mod = prepare_data_for_clustering(first_survey, survey_schema)
    second_df_mod = prepare_data_for_clustering(second_survey, survey_schema)
    mutual_ids = overlap(list(first_df_mod['id']), list(second_df_mod['id']))
    print('-' * 50)
    print('Reporting N')
    print('First Survey n: ', len(list(first_df_mod['id'])))
    print('Second Survey n: ', len(list(second_df_mod['id'])))
    print('Mutual n: ', len(mutual_ids))

    first_df_mod = first_df_mod.loc[first_df_mod['id'].isin(mutual_ids)]
    second_df_mod = second_df_mod.loc[second_df_mod['id'].isin(mutual_ids)]

    # Sort by id so the each student's interest is the same position in both lists
    first_df_mod.sort_values(by='id', axis=0, inplace=True, na_position='first')
    second_df_mod.sort_values(by='id', axis=0, inplace=True, na_position='first')

    first_interest = list(first_df_mod['Interest'])
    second_interest = list(second_df_mod['Interest'])
    return first_interest, second_interest


def change_in_interest_analysis(first_survey: pd.DataFrame, second_survey: pd.DataFrame, survey_schema: pd.DataFrame):
    first_interest, second_interest = get_cleaned_interest_data(first_survey, second_survey, survey_schema)

    check_normality_visually(first_interest, second_interest)
    check_normality(first_interest, second_interest)
    check_variances(first_interest, second_interest)
    compare_interest(first_interest, second_interest)

    plot_optional_reading_proportions([first_interest, second_interest])

    # diff = [m1 - m2 for m1, m2 in zip(first_interest, second_interest)]
    # check_normality(diff, [])
    # check_normality_visually(diff, [])


def check_normality_visually(first_interest: [], second_interest: [] = None):
    fig, ax = plt.subplots()
    bins = np.linspace(-2, 2, 70)

    ax.hist(first_interest, bins=bins, color='r', alpha=0.5, label='First Impressions Survey')

    if second_interest:
        ax.hist(second_interest, bins=bins, color='b', alpha=0.5, label='Second Impressions Survey')

    plt.legend()
    plt.show()


def check_normality(first_interest: [], second_interest: []):
    print('-' * 50)
    print('Check Normality of Data')
    print('H_0: The data is normally distributed\t', 'a = 0.05')
    print('Interpretation: p-value < 0.05 means we reject that this data follows a normal distribution')
    print('First Impressions Survey: ', test_normality(first_interest))

    if second_interest:
        print('Second Impressions Survey: ', test_normality(second_interest))


def test_normality(x: []):
    shapiro_wilks = scipy.stats.shapiro(x)
    return shapiro_wilks


def check_variances(first_interest: [], second_interest: []):
    print('-' * 50)
    print('Check Equality of Variance')
    var_1 = np.var(first_interest)
    var_2 = np.var(second_interest)
    print(var_1, var_2)
    print('-' * 50)
    print('Check Equality of Standard Deviation')
    sd_1 = np.std(first_interest)
    sd_2 = np.std(second_interest)
    print(sd_1, sd_2)


def compare_interest(first_interest: [], second_interest: []):
    """
    H_0 = That the medians are equal
    H_a = two-sided (so just that their means are not equal
    """
    wilcoxon = scipy.stats.wilcoxon(first_interest, second_interest)
    print(wilcoxon)


def plot_optional_reading_proportions(interest_dfs: [pd.DataFrame]):
    print('-' * 50)
    print('Optional Reading Analysis')
    print('Plot')
    for interest_df in interest_dfs:
        pass

    pass


def get_readers_for_page(module_num: int, page_num: int)

def student_interest_grouping():
    pass




def overlap(a: [], b: []) -> []:
    """Returns list of common elements in 2 input lists"""
    return [i for i in a if i in b]


def students_reading_module(module_num: int) -> dict:
    reading_logs_data = ReadingLogsData()
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()
    reading_duration_dict = reading_logs_data.get_reading_duration_dict()

    student_pages_read = defaultdict(int)

    for page_num in module_paragraphs_dict[f'{module_num}'].keys():
        page_reading_dict = reading_duration_dict[f'{module_num}-{page_num}']
        all_students = [int(data448_id) for data448_id in list(page_reading_dict.index)]
        for data448_id in all_students:
            student_pages_read[data448_id] += 1

    return student_pages_read


"""
1. In general, how many people read the optional modules?
    1.1. How fast did they read it?

2. For each optional module
    2.1. What did the readers say about their interest in HCI?
"""

"""
Programming Wise

Tasks
1. Return list of data448_ids for a module indicating who has any submissions for the whole module.
2. Return number of pages submitted by a given student in a module.

Visualizations
TABLE:
                       | % of students self reported scores (count) | % of students reading interviews (count) | % students reading module 11 (count) |
-----------------------|--------------------------------------------|------------------------------------------|--------------------------------------|
Positively Interested  |  55% (67 / 162)                            |   45% (35 / 67)
Negatively Interested  |  45% (78 / 162)                            |   45% (35 / 78)

Reading ANY of them


None
All
"""

"""
Presentation

By Survey
    By Question
            Table
"""
