from statistics import mean

import pandas as pd
import os

from sklearn.cluster import KMeans

from util import inertia_graph, kmeans_clustering, get_groups


def cluster_survey(data_path, output_path, categories):
    data = pd.read_csv(data_path)
    cluster_data = data.iloc[:, 1:6]
    file_name = os.path.basename(data_path)
    output_path_filename = os.path.join(output_path, file_name)
    get_groups(kmeans_clustering(3, 500, cluster_data, categories), data).to_csv(output_path_filename)
    inertia_graph(10, cluster_data)


def average_kmeans_iterations(data_path):
    data = pd.read_csv(data_path)
    cluster_data = data.iloc[:, 1:6]
    iterations = []
    for _ in range(500):
        model = KMeans(n_clusters=3, n_init=500).fit(cluster_data)
        iterations.append(model.n_iter_)
    print('Average k-means iterations: ', round(mean(iterations)))
