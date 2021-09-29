from scripts.clustering.clustering_model import cluster_survey
from scripts.clustering.data_preparation_for_clustering import prepare_data_hci

OUTPUT_DIRECTORY = "../../../data/processed"
HCI_SURVEY_DATA = "../../../data/raw/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "../../../data/processed/HCI_survey_schema.csv"
HCI_CLUSTER_DATA = "../../../data/processed/for_clustering_impression_survey1.csv"
STUDENT_GROUP_OUTPUT_DIRECTORY = "../../../data/student_group"

if __name__ == "__main__":
    prepare_data_hci(HCI_SURVEY_DATA, HCI_SURVEY_SCHEMA, OUTPUT_DIRECTORY)
    cluster_survey(HCI_CLUSTER_DATA, STUDENT_GROUP_OUTPUT_DIRECTORY)
