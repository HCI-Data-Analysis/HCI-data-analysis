import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
    This method takes in a dataframe for each page in a module and returns a two lists that contain the speedrunners,
    and the laggers outliers based on calculated IQR.
    :param module_id: id of module
    :param page_df: Dataframe of module page with completion times as columns
    :return: [speedrunners, laggers]
    """
    speedrunners = []
    laggers = []
    if not page_df.empty:
        page_df['timeTaken'] = page_df['end_time'] - page_df['start_time']

        quartiles = page_df[['timeTaken']].apply(get_q3_q1)
        q1 = quartiles['timeTaken'][1]
        q3 = quartiles['timeTaken'][0]

        # Multiply IQR by 1.5 due to outlier filter by the IQR rule
        iqr = page_df[['timeTaken']].apply(get_iqr)[0] * 1.5

        speedrunners = page_df.index[page_df['timeTaken'] < (q1 - iqr)].to_list()
        laggers = page_df.index[page_df['timeTaken'] > (q3 + iqr)].to_list()

        page_df['timeTakenSec'] = pd.to_numeric(page_df['timeTaken'] / 1000, downcast='integer')
        # Graph it
        sns.boxplot(x='timeTakenSec', data=page_df)
        plt.title(f'Boxplot for durations of module {module_id}')
        plt.axvline(x=int((q3 + iqr)/1000))
        plt.show()

    return speedrunners, laggers
