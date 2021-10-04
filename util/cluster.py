import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from statsmodels.multivariate.manova import MANOVA
from sklearn.cluster import KMeans
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
    # use elbow method to vaguely determine 3 clusters


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


def get_groups(labels, data):
    """
    Creates a dataframe with each column being a list of ids that belongs to the same group according to the
    clustering model.
    :param labels: a dataframe containing the labels the clustering model assigns each student.
    :param data: Source dataframe
    """

    labelled_students = pd.concat((data, labels), axis=1)
    labelled_students = labelled_students.rename({0: 'labels'}, axis=1)
    # labelled_students is a dataframe containing the source data and the labels clustering model assigns each student

    groups = labelled_students["labels"].unique()
    grouped_students = pd.DataFrame()

    for group in groups:
        grouped_student_list = [*labelled_students.loc[labelled_students["labels"] == group, "id"]]
        grouped_students["g" + str(group)] = pd.Series(grouped_student_list)

    return grouped_students


def manova_from_cluster_labels(manova_data: DataFrame, clusters_col_name) -> MANOVA:
    dependent_variables_list = list(manova_data.columns.values)
    parsed_dependent_variables = ' + '.join(filter(lambda var: var != clusters_col_name, dependent_variables_list))
    maov = MANOVA.from_formula(f'{parsed_dependent_variables} ~ {clusters_col_name}', data=manova_data)
    return maov


class StudentClusterModel:
    k = None
    clusters_col_name = 'labels'
    id_col_name = 'id'

    def __init__(self, data: DataFrame):
        self._indexed_data = data
        self._data = data.iloc[:, 1:len(data.columns)]

    def choose_k(self) -> int:
        """
        Decide k (the number of groups to cluster students into) and return it
        :return: k, the number of groups to divide students into
        """
        raise NotImplementedError

    def get_student_groups_df(self) -> DataFrame:
        raise NotImplementedError

    def get_num_groups(self) -> int:
        return self.k if self.k else self.choose_k()


class KMeansModel(StudentClusterModel):
    def __init__(self, *args, **kwargs):
        super(KMeansModel, self).__init__(*args, **kwargs)

    def _label_data_with_clusters(self, kmeans_model: KMeans, include_ids=False) -> DataFrame:
        data = self._indexed_data if include_ids else self._data

        student_group_labels_df = pd.DataFrame(kmeans_model.labels_)
        labelled_data = pd.concat((data, student_group_labels_df), axis=1)
        labelled_data = labelled_data.rename({0: self.clusters_col_name}, axis=1)

        if include_ids:
            labelled_data.set_index(self.id_col_name, inplace=True)
        return labelled_data

    def choose_k(self) -> int:
        lower_k = 2
        upper_k = len(self._data.index)
        highest_f_stat, chosen_k = 0, lower_k
        for k in range(lower_k, upper_k + 1):
            kmeans_model = KMeans(n_clusters=k).fit(self._data)
            manova_data = self._label_data_with_clusters(kmeans_model)
            manova_model = manova_from_cluster_labels(manova_data, self.clusters_col_name)
            # FIXME: should I be averaging all the different means of F value or use one, specifically
            current_f_stat = manova_model.mv_test().results[self.clusters_col_name]['stat']['F Value'].mean()
            # i.e. it will err on the side of less groups instead of more if F-statistic is equal
            if current_f_stat > highest_f_stat:
                highest_f_stat, chosen_k = current_f_stat, k

        self.k = chosen_k
        return chosen_k

    def fit_model(self) -> KMeans:
        k = self.choose_k()
        kmeans_model = KMeans(n_clusters=k).fit(self._data)
        return kmeans_model

    def get_student_groups_df(self) -> DataFrame:
        kmeans_model = self.fit_model()
        labelled_students = self._label_data_with_clusters(kmeans_model, include_ids=True)

        # # Plot the data when we have the correct labeled data.
        # df = labelled_students[labelled_students.index.notnull()]
        # sns.pairplot(data=df, hue='labels')
        # plt.show()

        dropped_columns = filter(lambda var: var != self.clusters_col_name, list(labelled_students.columns.values))
        labelled_students = labelled_students.drop(dropped_columns, axis=1)
        # FIXME: casting issue because of NA values
        # labelled_students = labelled_students.index.astype('int32')
        return labelled_students
