import os

import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
from statsmodels.multivariate.manova import MANOVA


def cluster_survey(data_path, output_path):
    data = pd.read_csv(data_path)
    file_name = os.path.basename(data_path)
    output_path_filename = os.path.join(output_path, file_name)
    kmeans_model = KMeansModel(data)
    kmeans_model.get_student_groups_df().to_csv(output_path_filename)

    # Plot the data when we have the correct labeled data.
    # sns.pairplot(data=labeled_data, hue='labels')
    # plt.show()


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
