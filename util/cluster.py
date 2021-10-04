import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from sklearn.cluster import KMeans, AgglomerativeClustering
import pandas as pd
import seaborn as sns
from sklearn.metrics import silhouette_score


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
    plt.title('Inertia Graph for K-means from 1-{}'.format(k))
    plt.show()
    # use elbow method to vaguely determine 3 clusters


def silhouette_graph(k, cluster_data):
    """
    Plots the silhouette values of kmeans model for 1 to n clusters.
    The silhouette method can then be used to subjectively determine how many clusters is ideal
    :param k: An integer which is the maximum number of clusters that is considered
    :param cluster_data: A dataframe which contains the data used to determine number of clusters
                        (independent variables only, the id column excluded).
    """
    silhouette = []
    K = range(2, k)
    for i in K:
        kmean_model = KMeans(n_clusters=i).fit(cluster_data)
        kmean_model.fit(cluster_data)
        silhouette.append(silhouette_score(cluster_data, labels=kmean_model.labels_, metric='cosine'))

    plt.plot(K, silhouette, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score Graph for K-means from 2-{}'.format(k))
    plt.show()


def correlation_heatmap(cluster_data, title):
    """
    Displays a heatmap based on the correlation of the data columns in cluster_data
    :param title: title of the plot that is generated
    :param cluster_data: the clustered dataframe to be plotted
    """
    plt.figure(figsize=(15, 10))
    plt.title(title)
    correlations = cluster_data.corr()
    sns.heatmap(round(correlations, 2), cmap='RdYlGn', annot=True, vmin=-1, vmax=1)
    plt.show()


def cluster_dendrogram(cluster_data, title):
    """
    Displays a cluster-dendrogram based on the correlation of the data columns in cluster_data
    :param title: title of the plot that is generated
    :param cluster_data: the clustered dataframe to be plotted
    """
    sns.clustermap(cluster_data.corr(), method='centroid', cmap='RdYlGn', annot=True, vmin=-1, vmax=1).fig.suptitle(
        title)
    plt.show()


def kmeans_clustering(n_clusters, cluster_data):
    """
    Runs the KMeans model of n_clusters.
    Creates a dataframe with the source and the label KMeans model assigns the student.
    :param n_clusters: number of clusters
    :param cluster_data: the data to use to determine clustering.
    :return:
    """
    kmeans = KMeans(n_clusters=n_clusters).fit(cluster_data)
    labels = pd.DataFrame(kmeans.labels_)
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)

    return labels


def ward_hierarchical_clustering(n_clusters, cluster_data):
    """
    Runs the Ward hierarchical model of n_clusters.
    Creates a dataframe with the source and the label Ward Hierarchical model assigns the student.
    :param n_clusters: number of clusters
    :param cluster_data: the data to use to determine clustering.
    :return:
    """
    hierarchy = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward').fit(cluster_data)
    labels = pd.DataFrame(hierarchy.labels_)
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)

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
