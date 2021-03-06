import os

import pandas as pd
from pandas import DataFrame

from schemas import ClusterSchema
from util import keep_latest_survey_attempt


def prepare_data_for_clustering(survey_df: DataFrame, schema_df: DataFrame, survey_path: str = None,
                                output_path: str = None) -> DataFrame:
    """
    Prepare the survey given in <survey_path> in ways that can be input into the clustering model.
    Outputs the file /data/processed/for_clustering_impression_survey.csv containing the above information
    :param survey_path: the path of the survey to be prepared
    :param output_path: the output path for the resulting CSV file
    :param survey_df: the survey dataframe to process.
    :param schema_df: a dataframe containing schema of the survey questions.
    :return: the processed dataframe.
    """

    survey_df = map_to_number(survey_df)
    convert_negative(survey_df, schema_df)
    average_score(survey_df, schema_df)

    prepared_df = prepare_dataframe_for_clustering(survey_df)

    if survey_path and output_path:
        file_name = os.path.basename(survey_path)
        output_dir = os.path.join(output_path, "for_clustering_" + file_name)
        prepared_df.to_csv(output_dir, index=False)

    return prepared_df


def map_to_number(survey_df: DataFrame) -> DataFrame:
    """
    Convert ordinal values to numerical representations.
    :param survey_df: a dataframe containing survey result.
    :return: the survey after being mapped to numbers.
    """
    survey_df = survey_df.replace("Strongly Disagree", -2)
    survey_df = survey_df.replace("Disagree", -1)
    survey_df = survey_df.replace("Neither Agree Nor Disagree", 0)
    survey_df = survey_df.replace("Agree", 1)
    survey_df = survey_df.replace("Strongly Agree", 2)
    return survey_df


def convert_negative(survey_df: DataFrame, schema_df: DataFrame):
    """
    Flip the response of negatively phrased question.
    :param survey_df: a dataframe containing survey result.
    :param schema_df: a dataframe containing the survey schema.
    """
    negatives_col_nums = schema_df[ClusterSchema.COL_NUM_1][schema_df[ClusterSchema.POSITIVE_NEGATIVE] < 1]
    for col in survey_df.iloc[:, negatives_col_nums]:
        survey_df[col] = survey_df[col].apply(lambda x: x * -1)


def average_score(survey_df: DataFrame, schema_df: DataFrame):
    """
    Compute the average score for each category.
    :param survey_df: a dataframe containing survey result.
    :param schema_df: a dataframe containing the survey schema.
    :return:
    """
    categories = schema_df[ClusterSchema.CATEGORY].unique()
    for category in categories:
        questions = schema_df[schema_df[ClusterSchema.CATEGORY] == category]
        question_col_num = questions[ClusterSchema.COL_NUM_1]
        question_df = survey_df.iloc[:, question_col_num]
        survey_df[category] = question_df.sum(axis=1) / len(question_col_num)


def prepare_dataframe_for_clustering(survey_df: DataFrame) -> DataFrame:
    """
    Prepare the specified dataframe for clustering.
    :param survey_df: the dataframe to prepare.
    :return: the prepared dataframe
    """
    survey_df = survey_df.drop(survey_df.columns[1], axis=1)

    student_info = survey_df.iloc[:, 0]
    aggregate = survey_df.iloc[:, -5:]
    result = pd.concat([student_info.reset_index(drop=True), aggregate.reset_index(drop=True)], axis=1)
    return result


def preprocess_survey(survey_df: DataFrame) -> DataFrame:
    """
    Gets the most recent attempt.
    :param survey_df: the dataframe to get the most recent attempt for.
    :return: the preprocessed dataframe.
    """
    temp_df = keep_latest_survey_attempt(survey_df)
    return temp_df
