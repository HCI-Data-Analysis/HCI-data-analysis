import pandas as pd

from scripts import prepare_data_for_clustering, cluster_survey, preprocess_survey

STUDENT_GROUP_OUTPUT_DIRECTORY = "data/processed"
HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
CLUSTER_CATEGORIES = ["Confidence", "Gender", "Professional", "Identity", "Interest"]

if __name__ == "__main__":
    # Get and pre-process survey data.
    survey_df = pd.read_csv(HCI_SURVEY_DATA)
    schema_df = pd.read_csv(HCI_SURVEY_SCHEMA)
    survey_df = preprocess_survey(survey_df)

    # Prepare data for clustering.
    processed_survey_df = prepare_data_for_clustering(survey_df, schema_df, HCI_SURVEY_DATA,
                                                      STUDENT_GROUP_OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    cluster_data = processed_survey_df.iloc[:, 1:6]
    cluster_survey(cluster_data, CLUSTER_CATEGORIES, 3)
