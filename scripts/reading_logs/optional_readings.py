import re
from collections import defaultdict

import pandas as pd

from schemas import CourseSchema
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


def analyze_optional_readings(survey_dfs: [pd.DataFrame], question: str):
    optional_module_data = {}
    for optional_module_num in CourseSchema.OPTIONAL_MODULES:
        student_page_reading_dict = students_reading_module(optional_module_num)
        optional_module_data[optional_module_num] = {
            'num_students_reading': len(student_page_reading_dict),
            'student_list': list(student_page_reading_dict.keys()),
            'student_reading_dict': student_page_reading_dict,
            'avg_pages_read': aggregate_and_sd(student_page_reading_dict.values())
        }

    all_survey_data = {}

    for survey_index, df in enumerate(survey_dfs):
        # survey_data = {
        #     answer: {} for answer in LIKERT_ANSWERS
        # }
        survey_data = defaultdict(dict)
        likert_data = get_likert_counts(df, question)
        for answer, student_list in likert_data.items():
            # if answer in survey_data:
            survey_data[answer]['num_students'] = len(student_list)
            for module_num, module_data in optional_module_data.items():
                survey_data[answer][f'num_reading_{module_num}'] = len(
                    overlap(student_list, module_data['student_list'])
                )
                pages_read = [
                    count for d_id, count in module_data['student_reading_dict'].items()
                    if d_id in student_list
                ]
                survey_data[answer][f'avg_pages_{module_num}'] = aggregate_and_sd(pages_read)
        all_survey_data[survey_index] = survey_data

    print_results(all_survey_data)


def print_results(all_survey_data: dict):
    for i, survey_data in all_survey_data.items():
        print(f'\t{i}')

        # Headers
        print(f'\tLikert Answer', end='')
        headers = list(all_survey_data[i].values())[0].keys()
        for header in headers:
            print(f'\t{header}', end='')
        print('\n', end='')

        for likert_answer, info in all_survey_data[i].items():
            print(f'\t{likert_answer}', end='')
            for header in headers:
                try:
                    print(f'\t{info[header]}', end='')
                except KeyError:
                    print(f'\tNA', end='')
            print('\n', end='')

        print('\n\n', end='')


def overlap(a: [], b: []) -> []:
    """Returns list of common elements in 2 input lists"""
    return [i for i in a if i in b]


def remove_id_prefix(col_name):
    regex = r'^([0-9]{7}: )'
    id_stripped_string = re.sub(regex, '', col_name)
    return id_stripped_string


def get_likert_counts(survey_df: pd.DataFrame, question_text: str) -> dict:
    """
    :return: dict<str, [int]> => {
        likert_answer_label: [data448_id...]
    }
    """
    student_answers = defaultdict(list)
    col_match_name = None
    for col_name in survey_df.columns:
        match_name = remove_id_prefix(col_name)
        if match_name.endswith(question_text):
            col_match_name = col_name
            break

    for data448_id, answer in zip(survey_df['id'], survey_df[col_match_name]):
        student_answers[answer].append(data448_id)

    return student_answers


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

None
All
"""

"""
Presentation

By Survey
    By Question
            Table
"""
