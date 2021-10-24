import pandas as pd

from scripts import clean_background_survey, cluster_survey, prepare_data_for_clustering, preprocess_survey

BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"
CLUSTER_CATEGORIES = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

if __name__ == "__main__":
    # Get and pre-process survey data.
    survey_df = pd.read_csv(BACKGROUND_SURVEY_DATA)
    survey_df = preprocess_survey(survey_df)

    # Clean and re-format background survey data.
    survey_df = clean_background_survey(survey_df)

    # Prepare data for clustering.
    processed_survey_df = prepare_data_for_clustering(survey_df, BACKGROUND_SURVEY_SCHEMA)

    # Execute clustering on the data and display graphs.
    cluster_survey(processed_survey_df, CLUSTER_CATEGORIES)
