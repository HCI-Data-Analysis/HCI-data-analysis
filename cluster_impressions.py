import pandas as pd

from scripts import prepare_data_for_clustering, cluster_survey, preprocess_survey

HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
CLUSTER_CATEGORIES = ["Confidence", "Gender", "Professional", "Identity", "Interest"]

if __name__ == "__main__":
    # Get and pre-process survey data.
    survey_df = pd.read_csv(HCI_SURVEY_DATA)
    survey_df = preprocess_survey(survey_df)

    # Prepare data for clustering.
    processed_survey_df = prepare_data_for_clustering(survey_df, HCI_SURVEY_SCHEMA)

    # Execute clustering on the data and display graphs.
    cluster_survey(processed_survey_df, CLUSTER_CATEGORIES)
