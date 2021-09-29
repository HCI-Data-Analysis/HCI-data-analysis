from scripts.clustering.background_survey_cleaning.background_survey_cleaning import clean_background_survey
from scripts.clustering.clustering_model import cluster_survey
from scripts.clustering.data_preparation_for_clustering import prepare_data_background

BACKGROUND_SURVEY_SCHEMA = "../../../data/processed/background_survey_schema.csv"
BACKGROUND_SURVEY_DATA = "../../../data/raw/background_survey.csv"
PROCESSED_BACKGROUND_SURVEY_DATA = "../../../data/processed/processed_background_survey.csv"
BACKGROUND_CLUSTER_DATA = "../../../data/processed/for_clustering_processed_background_survey.csv"
OUTPUT_DIRECTORY = "../../../data/processed"
STUDENT_GROUP_OUTPUT_DIRECTORY = "../../../data/student_group"

if __name__ == "__main__":
    # Pre-process background survey data.
    clean_background_survey(BACKGROUND_SURVEY_DATA, OUTPUT_DIRECTORY)

    # Prepare data for clustering.
    prepare_data_background(PROCESSED_BACKGROUND_SURVEY_DATA, BACKGROUND_SURVEY_SCHEMA, OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    cluster_survey(BACKGROUND_CLUSTER_DATA, STUDENT_GROUP_OUTPUT_DIRECTORY)
