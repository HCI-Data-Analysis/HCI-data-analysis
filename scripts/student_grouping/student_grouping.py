import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def categorize(x, threshold):
    """
    Uses the threshold value to map x onto [-1, 0, 1]

    :param x: the value to be categorized
    :param threshold: the threshold that determines what range of deviation is considered to be neutral
    :return: a categorized value belonging to the set: (-1, 0, 1)
    """
    if x >= threshold:
        return 1
    elif x <= (-1 * threshold):
        return -1
    else:
        return 0


def group_students(survey_path, facets):
    """
    Groups students based on the facet scores interpolated from the surveys into positive/neutral/negative groups and
    displays a histogram for each facet.

    :param survey_path: A string containing the filepath of the survey to use for the grouping.
    :param facets: A list of strings that represents the column names to be considered for grouping
    """
    survey = pd.read_csv(survey_path)
    grouping_map = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
    threshold = 0.1
    categories = [v for v in grouping_map.values()]
    for facet in facets:
        survey[facet] = survey[facet].apply(lambda x: categorize(x, threshold))
        survey[facet + " Value"] = pd.Categorical(survey[facet].map(grouping_map), categories=categories, ordered=True)
        figure, ax = plt.subplots()
        sns.histplot(survey, x=facet + " Value", ax=ax)
        ax.set_ylim(0, 170)
        plt.suptitle("Distribution for {}".format(facet))
        plt.show()
