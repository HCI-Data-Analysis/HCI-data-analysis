from scripts import clean_background_survey, cluster_survey, prepare_data_for_clustering

BACKGROUND_SURVEY_SCHEMA = "data/processed/background_survey_schema.csv"
BACKGROUND_SURVEY_DATA = "data/anonymized/background_survey.csv"
PROCESSED_BACKGROUND_SURVEY_DATA = "data/processed/processed_background_survey.csv"
BACKGROUND_CLUSTER_DATA = "data/processed/for_clustering_processed_background_survey.csv"
OUTPUT_DIRECTORY = "data/processed"
STUDENT_GROUP_OUTPUT_DIRECTORY = "data/processed/student_group"

if __name__ == "__main__":
    # Pre-process background survey data.
    clean_background_survey(BACKGROUND_SURVEY_DATA, OUTPUT_DIRECTORY)

    # Prepare data for clustering.
    prepare_data_for_clustering(PROCESSED_BACKGROUND_SURVEY_DATA, BACKGROUND_SURVEY_SCHEMA, OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    cluster_survey(BACKGROUND_CLUSTER_DATA, STUDENT_GROUP_OUTPUT_DIRECTORY)
