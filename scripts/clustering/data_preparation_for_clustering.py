import pandas as pd
from schemas import ClusterSchema


def prepare_data_for_clustering(survey_df, schema_path):
    """
    Prepare the survey given in <survey_path> in ways that can be input into the clustering model.
    Outputs the file /data/processed/for_clustering_impression_survey.csv containing the above information
    :param survey_df: The survey dataframe to process.
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :return: the processed dataframe.
    """
    data_schema_csv = pd.read_csv(schema_path)

    survey_df = map_to_number(survey_df)
    convert_negative(survey_df, data_schema_csv)
    average_score(survey_df, data_schema_csv)

    return prepare_dataframe_for_clustering(survey_df)


def map_to_number(survey):
    """
    Convert ordinal values to numerical representations.
    :param survey: a dataframe containing survey result.
    :return: the survey after being mapped to numbers.
    """
    survey = survey.replace("Strongly Disagree", -2)
    survey = survey.replace("Disagree", -1)
    survey = survey.replace("Neither Agree Nor Disagree", 0)
    survey = survey.replace("Agree", 1)
    survey = survey.replace("Strongly Agree", 2)
    return survey


def convert_negative(survey, schema_csv):
    """
    Flip the response of negatively phrased question.
    :param survey: a dataframe containing survey result.
    :param schema_csv: a dataframe containing the survey schema.
    """
    negatives_col_nums = schema_csv[ClusterSchema.COL_NUM_1][schema_csv[ClusterSchema.POSITIVE_NEGATIVE] < 1]
    for col in survey.iloc[:, negatives_col_nums]:
        survey[col] = survey[col].apply(lambda x: x * -1)


def average_score(survey, schema_csv):
    """
    Compute the average score for each category.
    :param survey: a dataframe containing survey result.
    :param schema_csv: a dataframe containing the survey schema.
    :return:
    """
    categories = schema_csv[ClusterSchema.CATEGORY].unique()
    for category in categories:
        questions = schema_csv[schema_csv[ClusterSchema.CATEGORY] == category]
        question_col_num = questions[ClusterSchema.COL_NUM_1]
        question_df = survey.iloc[:, question_col_num]
        survey[category] = question_df.sum(axis=1) / len(question_col_num)


def prepare_dataframe_for_clustering(survey):
    """
    Prepare the specified dataframe for clustering.
    :param survey: the dataframe to prepare.
    :return: the prepared dataframe
    """
    survey = survey.drop(survey.columns[1], axis=1)

    student_info = survey.iloc[:, 0]
    aggregate = survey.iloc[:, -5:]
    result = pd.concat([student_info.reset_index(drop=True), aggregate.reset_index(drop=True)], axis=1)
    return result
