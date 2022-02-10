import os
import json
import pandas as pd
import numpy as np

QUIZ_POINTS_POSSIBLE = 'quiz_points_possible'


def pre_test_first_attempt_grade(QUIZ_SCORE_JSON_PATH, data448_ids):
    """
    returns a dataframe containing the first attempt grade for each student's each pre-test
    :param QUIZ_SCORE_JSON_PATH: Path to the quizzes objects json files
    :return: a dictionary with keys of module_num and values of dataframes with student id and grade for that module
    """

    pre_test_quiz_ids = {
        198836: [1, 'Module 1'],
        283275: [2, 'Module 2'],
        202001: [3, 'Module 3'],
        217150: [4, 'Module 4'],
        217153: [5, 'Module 5'],
        317728: [6, 'Module 6'],
        210300: [7, 'Module 7'],
        329675: [8, 'Module 8'],
    }

    first_attempt_grade_df = pd.DataFrame(
        columns=['data448_id', 'quiz_id', 'percentage', 'module']
    )

    for i in os.listdir(QUIZ_SCORE_JSON_PATH):
        if i.endswith('.json'):
            full_path = os.path.join(QUIZ_SCORE_JSON_PATH, i)
            with open(full_path, 'r') as f:
                _gradebook = f.read()
                json_file = json.loads(_gradebook)
                if json_file:
                    for quiz_id in pre_test_quiz_ids.keys():
                        if quiz_id == json_file[0]['quiz_id']:
                            for json_block in json_file:
                                if json_block[QUIZ_POINTS_POSSIBLE] > 0:
                                    if json_block['attempt'] > 1:
                                        for previous_json_block in json_block['previous_submissions']:
                                            if previous_json_block['attempt'] == 1:
                                                json_block = previous_json_block

                                    student_first_attempt_grade = {
                                        'data448_id': json_block['user_id'],
                                        'quiz_id': json_block['quiz_id'],
                                        'percentage': json_block['score'] / json_block[QUIZ_POINTS_POSSIBLE] * 100,
                                        'module': pre_test_quiz_ids[json_block['quiz_id']][1]
                                    }
                                    first_attempt_grade_df = first_attempt_grade_df.append(student_first_attempt_grade,
                                                                               ignore_index=True)
                                    # except KeyError:
                                    #     print('nan')
    modules = first_attempt_grade_df['module'].unique()
    pre_test_student_average_dict = {}

    for module in modules:
        module_num = module.split(" ")[1]
        module_df = first_attempt_grade_df[first_attempt_grade_df['module'] == module][['data448_id', 'percentage']]
        pre_test_student_average_dict[module_num] = module_df

    return pre_test_student_average_dict
