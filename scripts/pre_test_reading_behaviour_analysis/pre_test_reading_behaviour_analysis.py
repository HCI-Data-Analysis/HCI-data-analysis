import numpy as np
from matplotlib import cm, pyplot as plt

from schemas import GradeBookSchema
from util import ReadingLogsData
import pandas as pd


def pre_test_reading_behaviour_analysis(gradebook):
    reading_logs_data = ReadingLogsData()

    data448_ids = gradebook[GradeBookSchema.STUDENT_ID]
    pre_test_1 = gradebook[GradeBookSchema.PRE_TEST_1]
    pre_test_2 = gradebook[GradeBookSchema.PRE_TEST_2]
    pre_test_3 = gradebook[GradeBookSchema.PRE_TEST_3]
    pre_test_4 = gradebook[GradeBookSchema.PRE_TEST_4]
    pre_test_5 = gradebook[GradeBookSchema.PRE_TEST_5]
    pre_test_6 = gradebook[GradeBookSchema.PRE_TEST_6]
    pre_test_7 = gradebook[GradeBookSchema.PRE_TEST_7]
    pre_test_8 = gradebook[GradeBookSchema.PRE_TEST_8]

    df_pre_test_reading_behaviour = pd.DataFrame(columns=[
        'data448_id', 'pre_test_1', 'module_reading_1', 'pre_test_2', 'module_reading_2',
        'pre_test_3', 'module_reading_3', 'pre_test_4', 'module_reading_4', 'pre_test_5', 'module_reading_5',
        'pre_test_6', 'module_reading_6', 'pre_test_7', 'module_reading_7', 'pre_test_8', 'module_reading_8'
    ])

    pre_test_modules = [
        (1, pre_test_1, GradeBookSchema.MAX_PRE_TEST_1), (2, pre_test_2, GradeBookSchema.MAX_PRE_TEST_2),
        (3, pre_test_3, GradeBookSchema.MAX_PRE_TEST_3), (4, pre_test_4, GradeBookSchema.MAX_PRE_TEST_4),
        (5, pre_test_5, GradeBookSchema.MAX_PRE_TEST_5), (6, pre_test_6, GradeBookSchema.MAX_PRE_TEST_6),
        (7, pre_test_7, GradeBookSchema.MAX_PRE_TEST_7), (8, pre_test_8, GradeBookSchema.MAX_PRE_TEST_8)
    ]
    for index, data448_id in enumerate(data448_ids):
        data448_id = int(data448_id)
        df_data = {'data448_id': data448_id}
        for [module, pre_test, max_pre_test_score] in pre_test_modules:
            try:
                [module_reading, module_reading_std] = reading_logs_data.module_reading_speed(module, data448_id)
            except KeyError:
                [module_reading, module_reading_std] = [None, None]
            df_data[f'pre_test_{module}'] = pre_test[index] / max_pre_test_score * 100
            df_data[f'module_reading_{module}'] = module_reading
        df_pre_test_reading_behaviour = df_pre_test_reading_behaviour.append(df_data, ignore_index=True)

    c_map = cm.get_cmap('Dark2')
    colours = c_map(np.linspace(0, 1, len(pre_test_modules)))

    for index, [module, _, _] in enumerate(pre_test_modules):
        values_x = [x for x in df_pre_test_reading_behaviour[f'pre_test_{module}']]
        values_y = [y for y in df_pre_test_reading_behaviour[f'module_reading_{module}']]
        plt.scatter(values_x, values_y, color=colours[index], label=f'Pre Test/Module {module}')
        print(f'{module}: Average Reading Speed: {np.mean([y for y in values_y if y > 0])}')
        print(f'{module}: Average Pre Test Grade: {np.mean([x for x in values_x if x > 0])}')
    plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.xlabel(f'Pre Test Scores (%)')
    plt.ylabel(f'Module Reading Speeds (words/minute)')
    plt.title(f'Pre Test Scores vs Module Reading Speeds')
    plt.tight_layout()
    plt.show()
