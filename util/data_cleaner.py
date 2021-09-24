import pandas as pd


def column_name_to_lower(df):
    """
    covert all column names to lowercase
    :param df: a dataframe with headers
    :return: the same dataframe but with all headers in lower case
    """
    cleaned = df.rename(str.lower, axis='columns')
    return cleaned
