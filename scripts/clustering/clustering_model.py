import os

import pandas as pd

from util import KMeansModel


def cluster_survey(data_path, output_path):
    data = pd.read_csv(data_path)
    file_name = os.path.basename(data_path)
    output_path_filename = os.path.join(output_path, file_name)
    kmeans_model = KMeansModel(data)
    kmeans_model.get_student_groups_df().to_csv(output_path_filename)

    # Plot the data when we have the correct labeled data.
    # sns.pairplot(data=labeled_data, hue='labels')
    # plt.show()
