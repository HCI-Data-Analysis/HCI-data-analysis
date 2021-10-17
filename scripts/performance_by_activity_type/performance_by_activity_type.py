import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from schemas import GradeBookSchema


def performance_by_activity_type(file_path):
    """

    :param file_path: the path to the gradebook csv.
    """
    gradebook = pd.read_csv(file_path)
    sns.displot(gradebook, x=GradeBookSchema.OVERALL_COURSE_SCORE, bins=10, kde=True)
    plt.show()
