import os

import pandas as pd

from scripts import clean_background_survey, cluster_survey, prepare_data_for_clustering, preprocess_survey
from scripts.clustering.clustering_model import KMeansModel
from util import mkdir_if_not_exists

BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"

OUTPUT_DIRECTORY = "data/processed"
STUDENT_GROUP_OUTPUT_DIRECTORY = "data/processed/student_group"

BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"
PROCESSED_BACKGROUND_SURVEY_DATA = "data/processed/processed_background_survey.csv"
BACKGROUND_CLUSTER_DATA = "data/processed/for_clustering_processed_background_survey.csv"


if __name__ == "__main__":
    mkdir_if_not_exists(OUTPUT_DIRECTORY)
    mkdir_if_not_exists(STUDENT_GROUP_OUTPUT_DIRECTORY)

    survey_df = pd.read_csv(BACKGROUND_SURVEY_DATA)
    survey_df = preprocess_survey(survey_df, clean_background_survey)
    # Pre-process background survey data.
    clean_background_survey(survey_df, OUTPUT_DIRECTORY)

    # Prepare data for clustering.
    cluster_data_df = prepare_data_for_clustering(PROCESSED_BACKGROUND_SURVEY_DATA, BACKGROUND_SURVEY_SCHEMA, OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    file_name = os.path.basename(BACKGROUND_CLUSTER_DATA)
    output_path_filename = os.path.join(BACKGROUND_CLUSTER_DATA, file_name)
    kmeans_model = KMeansModel(cluster_data_df)
    kmeans_model.get_student_groups_df().to_csv(output_path_filename)
