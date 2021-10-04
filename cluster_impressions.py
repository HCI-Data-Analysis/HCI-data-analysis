from scripts import prepare_data_for_clustering, cluster_survey

OUTPUT_DIRECTORY = "data/processed"
HCI_SURVEY_DATA = "data/anonymized/impression_survey1.csv"
HCI_SURVEY_SCHEMA = "data/processed/HCI_survey_schema.csv"
HCI_CLUSTER_DATA = "data/processed/for_clustering_impression_survey1.csv"
STUDENT_GROUP_OUTPUT_DIRECTORY = "data/student_group"

if __name__ == "__main__":
    # Prepare data for clustering.
    prepare_data_for_clustering(HCI_SURVEY_DATA, HCI_SURVEY_SCHEMA, OUTPUT_DIRECTORY)

    # Execute clustering on the data and display graphs.
    cluster_survey(HCI_CLUSTER_DATA, STUDENT_GROUP_OUTPUT_DIRECTORY)
