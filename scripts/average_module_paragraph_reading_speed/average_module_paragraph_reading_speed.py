from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from util import ReadingLogsData


def graph_average_module_paragraph_reading_speed(pages_difficulty_length_path):
    reading_logs_data = ReadingLogsData()
    processed_module_speed_data = pd.DataFrame(columns=[
        'module', 'speed', 'speed_std', 'difficulty', 'diff_std', 'par_len',
        'par_len_std', 'content_quiz_perf', 'content_quiz_perf_std'
    ])
    for file in Path(pages_difficulty_length_path).iterdir():
        if file.is_file():
            module_number = int(file.name.split('_')[2])
            pages_data = pd.read_csv(file.resolve())
            [speed, speed_std] = reading_logs_data.module_reading_speed(module_number)
            difficulties = []
            for page, row in pages_data.iterrows():
                difficulties.append(row['average_flesch_reading_ease'])
            difficulty = np.mean(difficulties)
            diff_std = np.std(difficulties)
            par_lengths = []
            for page, row in pages_data.iterrows():
                par_lengths.append(row['average_paragraph_length_words'])
            par_len = np.mean(par_lengths)
            par_len_std = np.std(par_lengths)
            content_quiz_perfs = []
            for page, row in pages_data.iterrows():
                content_quiz_data = reading_logs_data.page_content_quiz_num_attempts(module_number, page + 1)
                if content_quiz_data:
                    content_quiz_perfs.append(content_quiz_data[0])
            content_quiz_perf = np.mean(content_quiz_perfs)
            content_quiz_perf_std = np.std(content_quiz_perfs)
            processed_module_speed_data = processed_module_speed_data.append({
                'module': module_number,
                'speed': speed,
                'speed_std': speed_std,
                'difficulty': difficulty,
                'diff_std': diff_std,
                'par_len': par_len,
                'par_len_std': par_len_std,
                'content_quiz_perf': content_quiz_perf,
                'content_quiz_perf_std': content_quiz_perf_std
            }, ignore_index=True)
    processed_module_speed_data = processed_module_speed_data.sort_values(by='module')
    c_map = cm.get_cmap('Set3')
    colours = c_map(np.linspace(0, 1, len(processed_module_speed_data)))

    print('-------------------------------------')

    values_x = [x for x in processed_module_speed_data['difficulty']]
    values_y = [y for y in processed_module_speed_data['speed']]
    values_x_std = [std for std in processed_module_speed_data['diff_std']]
    values_y_std = [std for std in processed_module_speed_data['speed_std']]
    values_mod = [mod for mod in processed_module_speed_data['module']]
    for i, c in zip(range(len(values_x)), colours):
        plt.scatter(
            values_x[i], values_y[i], color=c,
            label=f'Module {int(values_mod[i])}'
        )
        print(f'Module {int(values_mod[i])}: '
              f'Speed: {round(values_y[i], 2)}, '
              f'Speed STD: {round(values_y_std[i], 2)}, '
              f'Difficulty: {round(values_x[i], 2)}, '
              f'Difficulty STD: {round(values_x_std[i], 2)})')
        plt.errorbar(values_x[i], values_y[i], xerr=values_x_std[i], yerr=values_y_std[i],
                     capsize=4, color=c, elinewidth=1)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.xlabel('Difficulty (flesch reading ease)')
    plt.ylabel('Speed (words/minute)')
    plt.title('Speed vs Difficulty of Modules')
    plt.tight_layout()
    plt.show()

    print('-------------------------------------')

    values_x = [x for x in processed_module_speed_data['difficulty']]
    values_y = [y for y in processed_module_speed_data['content_quiz_perf']]
    values_x_std = [std for std in processed_module_speed_data['diff_std']]
    values_y_std = [std for std in processed_module_speed_data['content_quiz_perf_std']]
    values_mod = [mod for mod in processed_module_speed_data['module']]
    for i, c in zip(range(len(values_x)), colours):
        plt.scatter(
            values_x[i], values_y[i], color=c,
            label=f'Module {int(values_mod[i])}'
        )
        print(f'Module {int(values_mod[i])}: '
              f'Content Quiz Performance: {round(values_y[i], 2)}, '
              f'Content Quiz Performance STD: {round(values_y_std[i], 2)}, '
              f'Difficulty: {round(values_x[i], 2)}, '
              f'Difficulty STD: {round(values_x_std[i], 2)})')
        plt.errorbar(values_x[i], values_y[i], xerr=values_x_std[i], yerr=values_y_std[i],
                     capsize=4, color=c, elinewidth=1)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.xlabel('Difficulty (flesch reading ease)')
    plt.ylabel('Content Quiz Performance')
    plt.title('Content Quiz Performance vs Difficulty of Modules')
    plt.tight_layout()
    plt.show()
