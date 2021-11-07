from cluster_background import CLUSTER_CATEGORIES
from scripts import group_students, performance_by_activity_type

BACKGROUND_SURVEY_PATH = "data/processed/for_clustering_background_survey.csv"
FILE_PATH = "data/anonymized/grade_book.csv"

if __name__ == "__main__":
    threshold = 0.5
    grouped_survey = group_students(BACKGROUND_SURVEY_PATH, CLUSTER_CATEGORIES, threshold)

    # Analysis for RQ: Do students that are more open perform better in group assignments overall?
    grouped_survey = grouped_survey.loc[:, grouped_survey.columns.isin(['id', 'Neuroticism_group'])]
    performance_by_activity_type(FILE_PATH, 2, grouped_survey)
