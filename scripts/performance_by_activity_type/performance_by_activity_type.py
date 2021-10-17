import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from schemas import GradeBookSchema


def performance_by_activity_type(file_path):
    """

    :param file_path: the path to the gradebook csv.
    """
    gradebook = pd.read_csv(file_path)
    overall_score_cols = [GradeBookSchema.OVERALL_COURSE_SCORE, GradeBookSchema.OVERALL_PROJECT_SCORE,
                          GradeBookSchema.OVERALL_PRE_POST_TESTS_SCORE, GradeBookSchema.OVERALL_MAIN_ACTIVITIES_SCORE,
                          GradeBookSchema.OVERALL_TUTORIAL_ACTIVITIES_SCORE, GradeBookSchema.OVERALL_READING_LOGS_SCORE]
    overall_score_data = gradebook.loc[:, gradebook.columns.isin(overall_score_cols)].replace({0: np.nan})
    sns.displot(overall_score_data, kind='kde', fill=True)
    plt.show()
    for col in overall_score_cols:
        sns.displot(overall_score_data[col], kind="kde", fill=True, color='pink')
        plt.axvline(overall_score_data[col].mean(), label='mean', linestyle=':', color='orange')
        plt.axvline(overall_score_data[col].std(), label='stdev', linestyle='--', color='purple')
        plt.legend(loc='upper left')
        plt.show()
