import pandas as pd
import seaborn as sns
import matplotlib as plt


def group_students(survey_path, facets):
    """
    groups students based on the OCEAN scores interpolated from the surveys

    :param survey_path: A string containing the filepath of the survey to use for the grouping.
    :param facets: A list of strings that represents the column names to be considered for grouping
    """
    survey = pd.read_csv(survey_path)
    for facet in facets:
        sns.displot(survey, x=facet)
        plt.show()
