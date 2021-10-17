import os

import pandas as pd
from pandas import DataFrame

from schemas import ClusterSchema, SurveySchema


def prepare_data_for_clustering(survey_path, schema_path, output_path, survey_df: DataFrame = None) -> DataFrame:
    """
    Prepare the survey given in <survey_path> in ways that can be input into the clustering model.
    The survey_df will be preprocessed, so might differ from raw data stored in the survey_path
    Outputs the file /data/processed/for_clustering_impression_survey.csv containing the above information
    :param survey_df: A dataframe for the survey in question.
    :param survey_path: A string containing the filepath of the survey being prepared.
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :param output_path: A string containing the path to output csv.
    """
    survey_df = survey_df if survey_df else pd.read_csv(survey_path)
    schema_df = pd.read_csv(schema_path)

    survey_df = map_to_number(survey_df)
    convert_negative(survey_df, schema_df)
    average_score(survey_df, schema_df)

    return prepare_csv_for_clustering(survey_df, survey_path, output_path)


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
    return result


def preprocess_survey(survey_df: DataFrame) -> DataFrame:
    temp_df = _keep_most_recent_attempt(survey_df)
    return temp_df


def _keep_most_recent_attempt(survey_df: DataFrame) -> DataFrame:
    survey_df = survey_df.sort_values(SurveySchema.ATTEMPT)
    survey_df.to_csv('sorted.csv')
    survey_df = survey_df[~survey_df.index.duplicated(keep='last')]
    survey_df.to_csv('all.csv')
    return survey_df
