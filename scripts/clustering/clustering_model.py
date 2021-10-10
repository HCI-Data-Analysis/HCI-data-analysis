import pandas as pd
import os

from util import inertia_graph, kmeans_clustering, get_groups, correlation_heatmap, ward_hierarchical_clustering, \
    cluster_dendrogram, silhouette_graph


def cluster_survey(data_path, output_path, categories):
    data = pd.read_csv(data_path)
    cluster_data = data.iloc[:, 1:6]
    k = 4
    title_str = 'Clustering with {} clusters'.format(k)
    file_name = os.path.basename(data_path)
    output_path_filename = os.path.join(output_path, file_name)
    get_groups(kmeans_clustering(3, 500, cluster_data, categories), data).to_csv(output_path_filename)
    groups = get_groups(kmeans_clustering(k, cluster_data), data)
    correlation_heatmap(groups, 'k-means ' + title_str)
    groups = get_groups(ward_hierarchical_clustering(k, cluster_data), data)
    cluster_dendrogram(groups, 'Ward Hierarchical ' + title_str)
    groups.to_csv(output_path_filename)
    inertia_graph(10, cluster_data)
    silhouette_graph(10, cluster_data)
