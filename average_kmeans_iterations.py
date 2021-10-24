import pandas as pd

from scripts import average_kmeans_iterations, prepare_data_for_clustering, clean_background_survey

HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"

if __name__ == "__main__":
    # Get data to run kmeans on from impression survey.
    survey_df = pd.read_csv(HCI_SURVEY_DATA)
    processed_impression_survey_df = prepare_data_for_clustering(survey_df, HCI_SURVEY_SCHEMA)

    # Get data to run kmeans on from background survey.
    survey_df = clean_background_survey(BACKGROUND_SURVEY_DATA)
    processed_background_survey_df = prepare_data_for_clustering(survey_df, BACKGROUND_SURVEY_SCHEMA)

    # Run kmeans for n-iter and determine the average time for convergence.
    average_kmeans_iterations(processed_impression_survey_df, 500)
    average_kmeans_iterations(processed_background_survey_df, 500)
