import os
import json
import pandas as pd
import numpy as np


def pre_test_get_first_attempt_grade(QUIZSCOREJSON_PATH):
    """
    returns a dataframe containing the first attempt grade for each student's each pre-test
    :param QUIZSCOREJSON_PATH: Path to the quizzes objects json files
    :return:
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

    QUIZ_POINTS_POSSIBLE = 'quiz_points_possible'

    for i in os.listdir(QUIZSCOREJSON_PATH):
        if i.endswith('.json'):
            full_path = os.path.join(QUIZSCOREJSON_PATH, i)
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
    return first_attempt_grade_df


def pre_test_first_attempt_grade_average(QUIZSCOREJSON_PATH, data448ids):
    students_df = pre_test_get_first_attempt_grade(QUIZSCOREJSON_PATH, data448ids)
    modules = students_df['module'].unique()
    module_average_grade = []

    for module in modules:
        module_average = np.mean(students_df[students_df['module'] == module]['percentage'])
        module_average_grade.append(module_average)
