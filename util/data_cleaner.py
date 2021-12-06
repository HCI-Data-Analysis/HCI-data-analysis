from pandas import DataFrame

from schemas import SurveySchema


def column_name_to_lower(df):
    """
    covert all column names to lowercase
    :param df: a dataframe with headers
    :return: the same dataframe but with all headers in lower case
    """
    cleaned = df.rename(str.lower, axis='columns')
    return cleaned


def keep_latest_survey_attempt(survey_df: DataFrame) -> DataFrame:
    """
    Keep the most recent attempt.
    :param survey_df: the dataframe with only the most recent attempt.
    :return: the dataframe.
    """
    survey_df = survey_df.sort_values(SurveySchema.ATTEMPT)
    survey_df = survey_df[~survey_df.index.duplicated(keep='last')]
    return survey_df
