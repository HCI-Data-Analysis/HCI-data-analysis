import pandas as pd
import os
from schemas import ClusterSchema


def prepare_data_hci(survey_path, schema_path, output_path):
    """
    Prepare the HCI impression survey given in <survey_path> in ways that can be input into the clustering model.
    Outputs the file /data/processed/for_clustering_impression_survey.csv containing the above information
    :param survey_path: A string containing the filepath of the survey being prepared.
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :param output_path: A string containing the path to output csv.
    """
    survey = pd.read_csv(survey_path)
    hci_schema_csv = pd.read_csv(schema_path)

    survey = map_to_number(survey)
    convert_negative(survey, hci_schema_csv)
    average_score(survey, hci_schema_csv)

    prepare_csv_for_clustering(survey, survey_path, output_path)


def prepare_data_background(survey_path, schema_path, output_path):
    """
    Prepare the background survey given in <survey_path> in ways that can be input into the clustering model.
    Outputs the file /data/processed/for_clustering_background_survey.csv containing the above information
    :param survey_path: A string containing the filepath of the survey being prepared.
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :param output_path: A string containing the path to output csv.
    """
    df = pd.read_csv(survey_path)
    background_schema_csv = pd.read_csv(schema_path)

    convert_negative(df, background_schema_csv)
    average_score(df, background_schema_csv)

    prepare_csv_for_clustering(df, survey_path, output_path)


def map_to_number(survey):
    """
    Convert ordinal values to numerical representations
    :param survey: a dataframe containing survey result
    """
    survey = survey.replace("Strongly Disagree", -2)
    survey = survey.replace("Disagree", -1)
    survey = survey.replace("Neither Agree Nor Disagree", 0)
    survey = survey.replace("Agree", 1)
    survey = survey.replace("Strongly Agree", 2)
    return survey


def convert_negative(survey, schema_csv):
    """
    Flip the response of negatively phrased question
    :param survey: a dataframe containing survey result
    :param schema_csv: a dataframe containing the survey schema
    """
    negatives_col_nums = schema_csv[ClusterSchema.COL_NUM_1][schema_csv[ClusterSchema.POSITIVE_NEGATIVE] < 1]
    for col in survey.iloc[:, negatives_col_nums]:
        survey[col] = survey[col].apply(lambda x: x * -1)


def average_score(survey, schema_csv):
    """
    Compute the average score for each category
    :param survey: a dataframe containing survey result
    :param schema_csv: a dataframe containing the survey schema
    :return:
    """
    categories = schema_csv[ClusterSchema.CATEGORY].unique()
    for category in categories:
        questions = schema_csv[schema_csv[ClusterSchema.CATEGORY] == category]
        question_col_num = questions[ClusterSchema.COL_NUM_1]
        question_df = survey.iloc[:, question_col_num]
        survey[category] = question_df.sum(axis=1) / len(question_col_num)


def prepare_csv_for_clustering(df, survey_path, output_path):
    """
    Export the specified dataframe to a csv file.
    :param df: the dataframe to export.
    :param survey_path: A string containing the path of the survey (for file name purposes).
    :param output_path: A string containing the path to output csv.
    """
    df = df.drop(df.columns[1], axis=1)

    student_info = df.iloc[:, 0]
    aggregate = df.iloc[:, -5:]
    result = pd.concat([student_info.reset_index(drop=True), aggregate.reset_index(drop=True)], axis=1)

    file_name = os.path.basename(survey_path)

    output_dir = os.path.join(output_path, "for_clustering_" + file_name)
    result.to_csv(output_dir, index=False)
