from scripts import clean_background_survey, cluster_survey, prepare_data_for_clustering

BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"
CLUSTER_CATEGORIES = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

if __name__ == "__main__":
    # Pre-process background survey data.
    survey_df = clean_background_survey(BACKGROUND_SURVEY_DATA)

    # Prepare data for clustering.
    processed_survey_df = prepare_data_for_clustering(survey_df, BACKGROUND_SURVEY_SCHEMA)

    # Execute clustering on the data and display graphs.
    cluster_survey(processed_survey_df, CLUSTER_CATEGORIES)
