import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from util import ReadingLogsData


def get_q3_q1(col):
    return np.percentile(col, [75, 25])


def get_iqr(col):
    """
    Return the Inter Quartile Range based on the values of Q3 and Q1
    :param col: an NP Series for which the IQR should be calculated
    :return: returns the value of the IQR for the specified numpy series
    """
    return np.subtract(*get_q3_q1(col))


def get_outlier_id_list(page_df, module_id):
    """
    This method takes in a duration dataframe for each page in a module and returns two lists that contain the
    speedrunners, and the laggers outliers based on calculated IQR.
    :param module_id: id of module-page
    :param page_df: Dataframe of module page with completion times as columns
    :return: [speedrunners, laggers]
    """
    speedrunners = []
    laggers = []
    module, page = module_id.split('-')
    reading_logs = ReadingLogsData()
    if not page_df.empty:
        page_df['speed'] = page_df.apply(lambda x: reading_logs.page_reading_speed(int(module), int(page), x.name)[0],
                                         axis=1)

        quartiles = page_df[['speed']].apply(get_q3_q1)
        q1 = quartiles['speed'][1]
        q3 = quartiles['speed'][0]

        # Multiply IQR by 1.5 due to outlier filter by the IQR rule
        iqr = page_df[['speed']].apply(get_iqr)[0] * 1.5

        speedrunners = page_df.index[page_df['speed'] < (q1 - iqr)].to_list()
        laggers = page_df.index[page_df['speed'] > (q3 + iqr)].to_list()

        # Graph it
        sns.boxplot(x='speed', data=page_df)
        plt.title(f'Boxplot for speeds of module {module_id}')
        plt.axvline(x=int((q3 + iqr)))
        plt.show()

    return speedrunners, laggers
