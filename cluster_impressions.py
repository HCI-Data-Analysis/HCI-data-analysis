import os
from pandas import pd

from scripts import prepare_data_for_clustering, cluster_survey, preprocess_survey
from scripts.clustering.clustering_model import KMeansModel

OUTPUT_DIRECTORY = "data/processed"
HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
HCI_CLUSTER_DATA = "data/processed/for_clustering_impression_survey1.csv"
STUDENT_GROUP_OUTPUT_DIRECTORY = "data/processed/student_group"

if __name__ == "__main__":
    # Prepare data for clustering.
    survey_df = pd.read_csv(HCI_SURVEY_DATA)
    survey_df = preprocess_survey(survey_df)
    cluster_data_df = prepare_data_for_clustering(HCI_SURVEY_DATA, HCI_SURVEY_SCHEMA, OUTPUT_DIRECTORY)

    file_name = os.path.basename(HCI_CLUSTER_DATA)
    output_path_filename = os.path.join(HCI_CLUSTER_DATA, file_name)

    # Execute clustering on the data and display graphs.
    # cluster_survey(HCI_CLUSTER_DATA, STUDENT_GROUP_OUTPUT_DIRECTORY)
    kmeans_model = KMeansModel(cluster_data_df)
    kmeans_model.get_student_groups_df().to_csv(output_path_filename)
