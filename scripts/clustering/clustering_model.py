from sklearn.cluster import KMeans
import pandas as pd
from schemas import DataFilesSchema
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv(DataFilesSchema.HCI_CLUSTER_DATA)
# data = pd.read_csv(DataFilesSchema.BACKGROUND_CLUSTER_DATA)
cluster_data = data.iloc[:, 2:7]


def inertia_graph(k):
    """
    Plots the inertia of kmeans model for 1 to n clusters.
    The elbow method can then be used to subjectively determine how many clusters is ideal
    :param k: maximum number of clusters that is considered
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


def kmeans_clustering(n_clusters):
    """
    Runs the KMeans model of n_clusters.
    Creates a dataframe with the source dataframe and the label KMeans model assigns the student.
    :param n_clusters: number of clusters
    :return:
    """
    kmeans = KMeans(n_clusters=n_clusters).fit(cluster_data)
    labels = pd.DataFrame(kmeans.labels_)
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)

    return labels


def pair_plot(labeled_data):
    """
    Creates a pair wise scatter plot of the clustered data
    :param labeled_data: A dataframe containing the source data (excluding the id column)
     and the labels clustering model assigns each student
    :return:
    """

    sns.pairplot(data=labeled_data, hue='labels')
    plt.show()


def get_groups(labels):
    """
    Creates a dataframe with each column being a list of ids that belongs to the same group according to the
    clustering model.
    :param labels: a dataframe containing the labels the clustering model assigns each student.
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


def export_to_csv(file_path):
    """
    Export the dataframe containing the groups of student ids into a csv.
    :param file_path: a string containing the file path of original data.
    :return:
    """
    file_name = os.path.basename(file_path)
    get_groups(kmeans_clustering(3)).to_csv(DataFilesSchema.STUDENT_GROUP_OUTPUT_DIRECTORY + file_name + ".csv")


if __name__ == '__main__':
    export_to_csv(DataFilesSchema.HCI_CLUSTER_DATA)
