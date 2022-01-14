from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from util import ReadingLogsData


def graph_average_module_paragraph_reading_speed(pages_difficulty_length_path):
    reading_logs_data = ReadingLogsData()
    processed_module_speed_data = pd.DataFrame(columns=['module', 'difficulty', 'speed', 'std'])
    for file in Path(pages_difficulty_length_path).iterdir():
        if file.is_file():
            module_number = int(file.name.split('_')[2])
            pages_data = pd.read_csv(file.resolve())
            speed = reading_logs_data.module_reading_speed(module_number, adjust_for_difficulty=True)
            difficulties = []
            for page, row in pages_data.iterrows():
                difficulties.append(row['average_flesch_reading_ease'])
            difficulty = np.mean(difficulties)
            std = np.std(difficulties)
            processed_module_speed_data = processed_module_speed_data.append({
                'module': module_number,
                'difficulty': difficulty,
                'speed': speed,
                'std': std
            }, ignore_index=True)
    processed_module_speed_data = processed_module_speed_data.sort_values(by='speed')
    c_map = cm.get_cmap('Set3')
    colours = c_map(np.linspace(0, 1, len(processed_module_speed_data)))
    values_x = [x for x in processed_module_speed_data['speed']]
    values_y = [y for y in processed_module_speed_data['difficulty']]
    values_std = [std for std in processed_module_speed_data['std']]
    values_mod = [mod for mod in processed_module_speed_data['module']]
    for i, c in zip(range(len(values_x)), colours):
        plt.scatter(
            values_x[i], values_y[i], color=c,
            label=f'Module {int(values_mod[i])}'
        )
        print(f'Module {int(values_mod[i])}: '
              f'(Speed: {round(values_x[i], 2)}, Ease: {round(values_y[i], 2)}, STD: {round(values_std[i], 2)})')
        plt.errorbar(values_x[i], values_y[i], yerr=values_std[i], capsize=4, color=c)
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.xlabel('Speed')
    plt.ylabel('Flesch Reading Ease')
    plt.title('Speed vs Flesch Reading Ease of Modules')
    plt.tight_layout()
    plt.show()
