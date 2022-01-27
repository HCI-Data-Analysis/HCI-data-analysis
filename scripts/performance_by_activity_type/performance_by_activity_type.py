import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import levene, f_oneway

from schemas import GradeBookSchema


def performance_by_activity_type(file_path, n_stddev, grouped_dataframe=None):
    """
    This method will extract data from the gradebook and graph the performance by activity type with plotted mean and standard deviations
    :param file_path: the path to the gradebook csv.
    :param n_stddev: the number of standard deviations on either side to be plotted for each graph
     :param grouped_dataframe: [optional] Specify a grouping for a single facet that will be merged with gradebook DF
     and display categorical data. Note: Dataframe should only have two columns: id and <FACET_NAME>_group
    """
    gradebook = pd.read_csv(file_path)
    overall_score_cols = [GradeBookSchema.STUDENT_ID, GradeBookSchema.OVERALL_COURSE_SCORE,
                          GradeBookSchema.OVERALL_PROJECT_SCORE, GradeBookSchema.OVERALL_PRE_POST_TESTS_SCORE,
                          GradeBookSchema.OVERALL_MAIN_ACTIVITIES_SCORE,
                          GradeBookSchema.OVERALL_TUTORIAL_ACTIVITIES_SCORE, GradeBookSchema.OVERALL_READING_LOGS_SCORE]
    overall_score_data = gradebook.loc[:, gradebook.columns.isin(overall_score_cols)].replace({0: np.nan})

    if grouped_dataframe is not None:
        # Retrieve the last column, which in this case will always be the second column
        facet_column_name = grouped_dataframe.columns[-1]
        overall_score_data = pd.merge(left=overall_score_data, right=grouped_dataframe,
                                      left_on=GradeBookSchema.STUDENT_ID, right_on='id')

    for col in overall_score_cols[1:]:

        if grouped_dataframe is not None:
            # If there are groups based on facets, plot categorized histograms
            g = sns.FacetGrid(overall_score_data, col=facet_column_name)
            g.map(sns.histplot, col)

            # Do Levene's test and ANOVA if Levene's test passes alpha value of 0.05
            # Generate columns for each category of facet
            positive_group = overall_score_data[overall_score_data[facet_column_name] == 'Positive'][col]
            neutral_group = overall_score_data[overall_score_data[facet_column_name] == 'Neutral'][col]
            negative_group = overall_score_data[overall_score_data[facet_column_name] == 'Negative'][col]

            # place non-empty DFs in params
            nonzero_params = [x for x in [positive_group, neutral_group, negative_group] if len(x) != 0]

            # run levene's test w/ alpha value of 0.05
            alpha = 0.05
            stat, p = levene(*nonzero_params)

            if p > alpha:
                # do ANOVA if levene's test passes
                print(f'ANOVA Results for {col} with facet {facet_column_name}:')
                print(f_oneway(*nonzero_params))
            else:
                print(f'levene test failed for column {col}')

        else:
            # set up plot
            mean = overall_score_data[col].mean()
            stdev = overall_score_data[col].std()
            max = overall_score_data[col].max()
            figure, ax = plt.subplots()

            # plot using seaborn histplot
            sns.histplot(overall_score_data, x=col, ax=ax, kde=True)

            # set the limits of the x-axis
            ax.set_xlim(0, max)

            # Plot mean and n_stddev std deviations on either side
            plt.axvline(mean, label='mean', linestyle=':', color='red')
            for i in range(1, n_stddev + 1):
                plt.axvline(mean - i * stdev, label='standard deviation', linestyle='--', color='purple')
                plt.axvline(mean + i * stdev, linestyle='--', color='purple')
            plt.legend()
            plt.suptitle('Density Distribution of {}'.format(col))

        plt.show()
