import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns


def plot_inertia_graph(max_k, cluster_data):
    """
    Plots the inertia of kmeans model for 1 to n clusters.
    The elbow method can then be used to subjectively determine how many clusters is ideal
    :param max_k: An integer which is the maximum number of clusters that is considered
    :param cluster_data: A dataframe which contains the data used to determine number of clusters
                        (independent variables only, the id column excluded).
    """
    inertia = []
    K = range(1, max_k)
    for i in K:
        kmeans_model = KMeans(n_clusters=i).fit(cluster_data)
        kmeans_model.fit(cluster_data)
        inertia.append(kmeans_model.inertia_)

    plt.plot(K, inertia, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Inertia')
    plt.show()


def plot_kmeans_clusters(labels, cluster_data, categories):
    """
    Runs the KMeans model of n_clusters.
    Creates a dataframe with the source and the label KMeans model assigns the student.
    :param labels: the labels dataframe for graphing.
    :param cluster_data: the data to use to determine clustering.
    :param categories: the categories to put on the axes.
    """
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)
    reversed_categories = categories[::-1]

    g = sns.pairplot(
        data=labeled_data,
        x_vars=categories,
        y_vars=reversed_categories,
        hue='labels'
    )
    for ax in g.axes[-1, :]:
        ax.set_xlim(-2, 2)
    for ay in g.axes[:, 0]:
        ay.set_ylim(-2, 2)
    plt.show()


def run_kmeans_clustering(n_clusters, n_init, cluster_data) -> KMeans:
    """
    Runs the KMeans model of n_clusters.
    :param n_clusters: number of clusters.
    :param n_init: A number indicating how many times KMeans should be run.
    :param cluster_data: the data to use to determine clustering.
    :return: the kmeans model.
    """
    return KMeans(n_clusters=n_clusters, n_init=n_init).fit(cluster_data)


def get_labels(kmeans: KMeans) -> DataFrame:
    """
    Returns the labels after clustering.
    :param kmeans: the model kmeans model.
    """
    return pd.DataFrame(kmeans.labels_)
