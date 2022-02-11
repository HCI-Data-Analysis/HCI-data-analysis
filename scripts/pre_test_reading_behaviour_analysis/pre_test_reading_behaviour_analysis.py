import json
import os

import numpy as np
from matplotlib import pyplot as plt

from util import ReadingLogsData
import pandas as pd
import seaborn as sns


def pre_test_reading_behaviour_analysis(QUIZSCOREJSON_PATH):
    reading_logs_data = ReadingLogsData()

    df_first_attempt = pd.DataFrame(
        columns=['data448_id', 'quiz_id', 'percentage', 'reading_speed', 'module']
    )
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
                                    try:
                                        [module_reading, module_reading_std] = reading_logs_data.module_reading_speed(
                                            pre_test_quiz_ids[json_block['quiz_id']][0], json_block['user_id'])
                                        student_first_attempt_data = {
                                            'data448_id': json_block['user_id'],
                                            'quiz_id': json_block['quiz_id'],
                                            'reading_speed': module_reading,
                                            'reading_speed_std': module_reading_std,
                                            'percentage': json_block['score'] / json_block[QUIZ_POINTS_POSSIBLE] * 100,
                                            'module': pre_test_quiz_ids[json_block['quiz_id']][1]
                                        }
                                        df_first_attempt = df_first_attempt.append(student_first_attempt_data,
                                                                                   ignore_index=True)
                                    except KeyError:
                                        pass

    g = sns.lmplot(x="percentage", y="reading_speed", col="module", hue="module", data=df_first_attempt,
                   col_wrap=4, ci=None, palette="muted", height=4,
                   scatter_kws={"s": 50, "alpha": 1})
    g.set_axis_labels("First Attempt Pre Test Score (%)", "Reading Speed (WPM)")
    plt.show()
    g = sns.lmplot(x="percentage", y="reading_speed", data=df_first_attempt)
    g.set_axis_labels("First Attempt Pre Test Score (%)", "Reading Speed (WPM)")
    plt.show()

    for quiz_id in pre_test_quiz_ids.keys():
        temp_df = df_first_attempt[df_first_attempt['quiz_id'] == quiz_id]
        print(pre_test_quiz_ids[quiz_id][1], 'averages:')
        print('Average reading speed:', np.mean(temp_df['reading_speed']))
        print('Average percentage:', np.mean(temp_df['percentage']))
        print('-------')

    print('Overall averages:')
    print('Average reading speed:', np.mean(df_first_attempt['reading_speed']))
    print('Average percentage:', np.mean(df_first_attempt['percentage']))
    print('-------')

    for quiz_id in pre_test_quiz_ids.keys():
        temp_df = df_first_attempt[df_first_attempt['quiz_id'] == quiz_id]
        print(pre_test_quiz_ids[quiz_id][1], 'correlations:')
        corr = np.corrcoef(temp_df['reading_speed'], temp_df['percentage'])
        print(corr)
        print('R^2:')
        print(corr[0][1]**2)
        print('-------')

    print('Overall correlations:')
    corr = np.corrcoef(df_first_attempt['reading_speed'], df_first_attempt['percentage'])
    print(corr)
    print('R^2:')
    print(corr[0][1]**2)
    print('-------')
