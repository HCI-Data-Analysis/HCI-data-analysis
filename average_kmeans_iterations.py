import pandas as pd

from scripts import average_kmeans_iterations, prepare_data_for_clustering, clean_background_survey

HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"

if __name__ == "__main__":
    # Get data to run kmeans on from impression survey.
    impression_survey_df = pd.read_csv(HCI_SURVEY_DATA)
    impression_schema_df = pd.read_csv(HCI_SURVEY_SCHEMA)
    processed_impression_survey_df = prepare_data_for_clustering(impression_survey_df, impression_schema_df)

    # Get data to run kmeans on from background survey.
    background_survey_df = pd.read_csv(BACKGROUND_SURVEY_DATA)
    background_survey_df = clean_background_survey(background_survey_df)
    background_schema_df = pd.read_csv(BACKGROUND_SURVEY_SCHEMA)
    processed_background_survey_df = prepare_data_for_clustering(background_survey_df, background_schema_df)

    # Run kmeans for n-iter and determine the average time for convergence.
    impression_cluster_data = processed_impression_survey_df.iloc[:, 1:6]
    background_cluster_data = processed_background_survey_df.iloc[:, 1:6]
    average_kmeans_iterations(impression_cluster_data, 500, 3)
    average_kmeans_iterations(background_cluster_data, 500, 3)
