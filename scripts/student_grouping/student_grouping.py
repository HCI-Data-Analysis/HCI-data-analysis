import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame
import statsmodels.api as sm
from statsmodels.formula.api import ols


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


def group_students(survey_path, facets, threshold) -> DataFrame:
    """
    Groups students based on the facet scores interpolated from the surveys into positive/neutral/negative groups and
    displays a histogram for each facet.

    :param threshold: The boundaries for the neutral group: [-threshold, +threshold]
    :param survey_path: A string containing the filepath of the survey to use for the grouping.
    :param facets: A list of strings that represents the column names to be considered for grouping
    """
    survey = pd.read_csv(survey_path)
    grouping_map = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
    categories = [v for v in grouping_map.values()]
    for facet in facets:
        survey["standardized_" + facet] = survey[facet].apply(lambda x: categorize(x, threshold))
        survey[facet + "_group"] = pd.Categorical(survey["standardized_" + facet].map(grouping_map),
                                                  categories=categories, ordered=True)
        figure, ax = plt.subplots()
        sns.histplot(survey, x=facet + "_group", ax=ax)
        ax.set_ylim(0, 170)
        plt.suptitle("Distribution for {}".format(facet))
        plt.show()
    return survey

# ANOVA CODE (using directions from https://www.pythonfordatascience.org/anova-python/#anova_statsmodels)
# model = ols('Openness ~ C(standardized_Openness)', data=survey).fit()
# anova_table = sm.stats.anova_lm(model, typ=2)
