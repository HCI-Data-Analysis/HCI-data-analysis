import pandas as pd
import seaborn as sns
import os
from util import inertia_graph, kmeans_clustering, get_groups


def cluster_survey(data_path, output_path):
    data = pd.read_csv(data_path)
    cluster_data = data.iloc[:, 1:6]
    file_name = os.path.basename(data_path)
    output_path_filename = os.path.join(output_path, file_name + '.csv')
    get_groups(kmeans_clustering(3, cluster_data), data).to_csv(output_path_filename)
    inertia_graph(10, cluster_data)

    # Plot the data when we have the correct labeled data.
    # sns.pairplot(data=labeled_data, hue='labels')
    # plt.show()
