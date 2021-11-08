import cluster_background
import cluster_impressions
from scripts import group_students, performance_by_activity_type

BACKGROUND_SURVEY_PATH = "data/processed/for_clustering_background_survey.csv"
HCI_SURVEY_DATA = "data/processed/for_clustering_impression_survey1.csv"
FILE_PATH = "data/anonymized/grade_book.csv"

if __name__ == "__main__":
    threshold = 0.5

    # # Background Survey
    # grouped_survey = group_students(BACKGROUND_SURVEY_PATH, cluster_background.CLUSTER_CATEGORIES, threshold)
    #
    # # Sample Analysis for RQ: Do students that are more open perform better in group assignments overall?
    # grouped_survey = grouped_survey.loc[:, grouped_survey.columns.isin(['id', 'Openness_group'])]
    # performance_by_activity_type(FILE_PATH, 2, grouped_survey)

    # Impressions Survey
    grouped_survey = group_students(HCI_SURVEY_DATA, cluster_impressions.CLUSTER_CATEGORIES, threshold)

    # Sample Analysis for RQ: Do students that are more confident perform better in group assignments overall?
    grouped_survey = grouped_survey.loc[:, grouped_survey.columns.isin(['id', 'Gender_group'])]
    performance_by_activity_type(FILE_PATH, 2, grouped_survey)
