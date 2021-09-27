from sklearn.cluster import KMeans
import pandas as pd
from schemas import data_files
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("../" + data_files.HCI_CLUSTER_DATA)
# data = pd.read_csv("../" + data_files.BACKGROUND_CLUSTER_DATA)
cluster_data = data.iloc[:, 2:7]


def elbow_method():
    inertia = []
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(cluster_data)
        kmeanModel.fit(cluster_data)
        inertia.append(kmeanModel.inertia_)

    plt.plot(K, inertia, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Inertia')
    plt.show()
    # use elbow method to vaguely determine 3 clusters


def kmeans_clustering(n_clusters):
    kmeans = KMeans(n_clusters=n_clusters).fit(cluster_data)
    labels = pd.DataFrame(kmeans.labels_)
    labeled_data = pd.concat((cluster_data, labels), axis=1)
    labeled_data = labeled_data.rename({0: 'labels'}, axis=1)

    sns.pairplot(data=labeled_data, hue='labels')
    plt.show()

    return labels


def get_groups(labels):
    labeled_students = pd.concat((data, labels), axis=1)
    labeled_students = labeled_students.rename({0: 'labels'}, axis=1)

    groups = labeled_students["labels"].unique()
    grouped_students = pd.DataFrame()

    grouped_students0 = [*labeled_students.loc[labeled_students["labels"] == 0, "id"]]
    grouped_students1 = [*labeled_students.loc[labeled_students["labels"] == 1, "id"]]
    grouped_students2 = [*labeled_students.loc[labeled_students["labels"] == 2, "id"]]

    grouped_students = pd.DataFrame(
        {"g0": pd.Series(grouped_students0), "g1": pd.Series(grouped_students1), "g2": pd.Series(grouped_students2)})

    grouped_students.to_csv("../../../data/HCI_survey_group.csv")


if __name__ == '__main__':
    get_groups(kmeans_clustering(3))
