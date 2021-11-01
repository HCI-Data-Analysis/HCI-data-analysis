from cluster_background import CLUSTER_CATEGORIES
from scripts import group_students

BACKGROUND_SURVEY_PATH = "data/processed/for_clustering_background_survey.csv"

if __name__ == "__main__":
    group_students(BACKGROUND_SURVEY_PATH, CLUSTER_CATEGORIES)
