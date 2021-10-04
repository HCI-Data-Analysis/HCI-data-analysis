import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns


def inertia_graph(k, cluster_data):
    """
    Plots the inertia of kmeans model for 1 to n clusters.
    The elbow method can then be used to subjectively determine how many clusters is ideal
    :param k: An integer which is the maximum number of clusters that is considered
    :param cluster_data: A dataframe which contains the data used to determine number of clusters
                        (independent variables only, the id column excluded).
    """
    inertia = []
    K = range(1, k)
    for i in K:
        kmean_model = KMeans(n_clusters=i).fit(cluster_data)
        kmean_model.fit(cluster_data)
        inertia.append(kmean_model.inertia_)

    plt.plot(K, inertia, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Inertia')
    plt.show()
    # use elbow method to vaguely determine 3 clusters


def kmeans_clustering(n_clusters, n_init, cluster_data):
    """
    Runs the KMeans model of n_clusters.
    Creates a dataframe with the source and the label KMeans model assigns the student.
    :param n_clusters: number of clusters
    :param n_init: A number indicating how many times KMeans should be run
    :param cluster_data: the data to use to determine clustering.
    :return:
    """
    kmeans = KMeans(n_clusters=n_clusters, n_init=n_init).fit(cluster_data)
    labels = pd.DataFrame(kmeans.labels_)
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)

    g = sns.pairplot(data=labeled_data, hue='labels')
    for ax in g.axes[-1, :]:
        ax.set_xlim(-2, 2)
    for ay in g.axes[:, 0]:
        ay.set_ylim(-2, 2)
    plt.show()

    return labels


def get_groups(labels, data):
    """
    Creates a dataframe with each column being a list of ids that belongs to the same group according to the
    clustering model.
    :param labels: a dataframe containing the labels the clustering model assigns each student.
    :param data: Source dataframe
    """

    labeled_students = pd.concat((data, labels), axis=1)
    labeled_students = labeled_students.rename({0: 'labels'}, axis=1)
    # labeled_students is a dataframe containing the source data and the labels clustering model assigns each student

    groups = labeled_students["labels"].unique()
    grouped_students = pd.DataFrame()

    for group in groups:
        grouped_student_list = [*labeled_students.loc[labeled_students["labels"] == group, "id"]]
        grouped_students["g" + str(group)] = pd.Series(grouped_student_list)

    return grouped_students
