import pandas as pd

from scripts import clustering_tendency, clean_background_survey, preprocess_survey, prepare_data_for_clustering

HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"

BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"

if __name__ == "__main__":
    # Background Survey
    df_background_survey = pd.read_csv(BACKGROUND_SURVEY_DATA)
    schema_df = pd.read_csv(BACKGROUND_SURVEY_SCHEMA)

    df_background_survey = preprocess_survey(df_background_survey)
    df_background_survey = clean_background_survey(df_background_survey)
    processed_background_survey_df = prepare_data_for_clustering(df_background_survey, schema_df)
    df_background_survey = processed_background_survey_df.iloc[:, 1:6]

    clustering_tendency(df_background_survey)

    # Impressions Survey
    impression_survey_df = pd.read_csv(HCI_SURVEY_DATA)
    schema_df = pd.read_csv(HCI_SURVEY_SCHEMA)

    impression_survey_df = preprocess_survey(impression_survey_df)
    processed_impression_survey_df = prepare_data_for_clustering(impression_survey_df, schema_df)
    impression_survey_df = processed_impression_survey_df.iloc[:, 1:6]

    clustering_tendency(impression_survey_df)
