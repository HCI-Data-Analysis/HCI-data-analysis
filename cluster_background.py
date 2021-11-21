import pandas as pd

from scripts import clean_background_survey, cluster_survey, prepare_data_for_clustering, preprocess_survey

STUDENT_GROUP_OUTPUT_DIRECTORY = "data/processed"
BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"
CLUSTER_CATEGORIES = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

if __name__ == "__main__":
    # Get and pre-process survey data.
    survey_df = pd.read_csv(BACKGROUND_SURVEY_DATA)
    schema_df = pd.read_csv(BACKGROUND_SURVEY_SCHEMA)
    survey_df = preprocess_survey(survey_df)

    # Clean and re-format background survey data.
    survey_df = clean_background_survey(survey_df)

    # Prepare data for clustering.
    processed_survey_df = prepare_data_for_clustering(survey_df, schema_df, BACKGROUND_SURVEY_DATA,
                                                      STUDENT_GROUP_OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    cluster_data = processed_survey_df.iloc[:, 1:6]
    cluster_survey(cluster_data, CLUSTER_CATEGORIES, 3)
