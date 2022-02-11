from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from util import ReadingLogsData


def graph_average_module_paragraph_reading_speed(pages_difficulty_length_path):
    reading_logs_data = ReadingLogsData()
    processed_module_speed_data = pd.DataFrame(columns=[
        'module', 'page', 'speed', 'speed_std', 'difficulty', 'diff_std', 'par_len',
        'par_len_std', 'content_quiz_perf', 'content_quiz_perf_std'
    ])
    for file in Path(pages_difficulty_length_path).iterdir():
        if file.is_file():
            module_number = int(file.name.split('_')[2])
            pages_data = pd.read_csv(file.resolve())
            for page, row in pages_data.iterrows():
                print(module_number, page)
                [speed, speed_std] = reading_logs_data.page_reading_speed(module_number, page + 1)
                cqp_t = reading_logs_data.page_content_quiz_num_attempts(module_number, page + 1)
                processed_module_speed_data = processed_module_speed_data.append({
                    'module': module_number,
                    'page': page + 1,
                    'speed': speed,
                    'speed_std': speed_std,
                    'difficulty': 100 - row['average_flesch_reading_ease'],
                    'diff_std': 0,
                    'par_len': row['average_paragraph_length_words'],
                    'par_len_std': 0,
                    'content_quiz_perf': cqp_t[0] if cqp_t else None,
                    'content_quiz_perf_std': cqp_t[1] if cqp_t else None
                }, ignore_index=True)
    print(processed_module_speed_data.to_string())

    g = sns.lmplot(x="difficulty", y="speed", col="module", hue="module",
                   data=processed_module_speed_data,
                   col_wrap=5, ci=None, palette="muted", height=4,
                   scatter_kws={"s": 50, "alpha": 1})
    g.set_axis_labels("Difficulty (100-Flesch)", "Reading Speed (WPM)")
    plt.show()
    g = sns.lmplot(x="difficulty", y="speed",
                   data=processed_module_speed_data)
    g.set_axis_labels("Difficulty (100-Flesch)", "Reading Speed (WPM)")
    plt.show()

    print('Speed vs difficulty correlation coefficient')
    corr = np.corrcoef(processed_module_speed_data['difficulty'], processed_module_speed_data['speed'])
    print(corr)
    print('R^2')
    print(corr[0][1]**2)
    print('-----------')
    print('Speed vs difficulty averages')
    print('Speed:', np.average(processed_module_speed_data['speed']))
    print('Difficulty:', np.average(processed_module_speed_data['difficulty']))
    print('-----------')

    g = sns.lmplot(x="difficulty", y="content_quiz_perf", col="module", hue="module",
                   data=processed_module_speed_data,
                   col_wrap=5, ci=None, palette="muted", height=4,
                   scatter_kws={"s": 50, "alpha": 1})
    g.set_axis_labels("Difficulty (100-Flesch)", "Content Quiz Performance (Extra attempt ratio)")
    plt.show()
    g = sns.lmplot(x="difficulty", y="content_quiz_perf",
                   data=processed_module_speed_data)
    g.set_axis_labels("Difficulty (100-Flesch)", "Content Quiz Performance (Extra attempt ratio)")
    plt.show()

    qp = []
    df = []
    for i, x in enumerate(processed_module_speed_data['content_quiz_perf']):
        if x > 0:
            qp.append(x)
            df.append(processed_module_speed_data['difficulty'][i])

    print('Quiz perf vs difficulty correlation coefficient')
    corr = np.corrcoef(df, qp)
    print(corr)
    print('R^2')
    print(corr[0][1]**2)
    print('-----------')
    print('Quiz perf vs difficulty averages')
    print('Quiz perf:', np.average(qp))
    print('Difficulty:', np.average(df))
    print('-----------')
