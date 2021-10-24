from util import inertia_graph, kmeans_clustering, get_groups


def cluster_survey(survey_df, categories):
    """
    Performs clustering on the dataframe, and graphs the inertia as graph for the specified dataframe.
    :param survey_df: the processed dataframe to perform clustering on.
    :param categories: the categories for labels on the pair-plot.
    :return: the student groups as a dataframe.
    """
    cluster_data = survey_df.iloc[:, 1:6]
    student_groups = get_groups(kmeans_clustering(3, 500, cluster_data, categories), survey_df)
    inertia_graph(10, cluster_data)
    return student_groups
