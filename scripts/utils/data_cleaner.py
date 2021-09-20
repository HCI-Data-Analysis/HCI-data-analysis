import pandas as pd



def trim_white_spaces(df):
    '''
    trim all leading and trailing whitespaces of any string for every element including column names in the df
    :param df: any dataframe with header
    :return: same dataframe with all leading/trailing whitespaces trimmed
    '''
    cleaned = trim_white_spaces_in_header(df)
    cleaned = trim_white_space_in_data(cleaned)

    return cleaned


def trim_white_spaces_in_header(df):
    '''
     trim all leading and trailing whitespaces of all column names in the df
    :param df: any dataframe with header
    :return: same dataframe with all leading/trailing whitespaces in headers trimmed
    '''

    df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x, inplace=True)
    return df

def column_name_to_lower(df):
    '''
    covert all column names to lowercase
    :param df: a dataframe with headers
    :return: the same dataframe but with all headers in lower case
    '''
    cleaned = df.rename(str.lower, axis='columns')
    return cleaned


def trim_white_space_in_data(df):
    '''
     trim all leading and trailing whitespaces of all elements in the df
    :param df: any dataframe
    :return: same dataframe with all leading/trailing whitespaces trimmed
    '''
    cleaned = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return cleaned


def drop_unamed_columns(df):
    '''
    drops any unamed columns
    :param df: any df
    :return: same df with all unamed columns dropped
    '''
    cleaned = df.loc[:, ~df.columns.str.contains('^Unamed')]
    return cleaned

