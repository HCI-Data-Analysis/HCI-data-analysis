from pandas import DataFrame
from statsmodels.multivariate.manova import MANOVA

from util import plot_inertia_graph, plot_kmeans_clusters, get_labels, run_kmeans_clustering


def cluster_survey(cluster_data, categories, k):
    """
    Performs clustering on the dataframe, and graphs the inertia as graph for the specified dataframe.
    :param cluster_data: the processed dataframe to perform clustering on.
    :param categories: the categories for labels on the pair-plot.
    :param k: the number of clusters.
    """
    kmeans = run_kmeans_clustering(k, 500, cluster_data)
    labels = get_labels(kmeans)
    plot_kmeans_clusters(labels, cluster_data, categories)
    plot_inertia_graph(10, cluster_data)


def manova_from_cluster_labels(manova_data: DataFrame, clusters_col_name) -> MANOVA:
    dependent_variables_list = list(manova_data.columns.values)
    parsed_dependent_variables = ' + '.join(filter(lambda var: var != clusters_col_name, dependent_variables_list))
    manova = MANOVA.from_formula(f'{parsed_dependent_variables} ~ {clusters_col_name}', data=manova_data)
    return manova


def get_f_stat_from_manova(manova: MANOVA, clusters_col_name):
    current_f_stat = manova.mv_test().results[clusters_col_name]['stat']['F Value'].mean()
    return current_f_stat
