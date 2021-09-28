import re
import pandas as pd
import os
from schemas import data_files

# BACKGROUND_SURVEY_SCHEMA = "../../../data/background_survey_schema.csv"
# BACKGROUND_SURVEY_DATA = "../../../data/background_survey.csv"
# OUTPUT_DIRECTORY = "../../../data"
# FILE_NAME = "processed_background_survey"


def prepare_df():
    """
    Prepares and cleans the dataframe so it is possible to use it for clustering.
    Fixes the single column with all the questions in it.
    """
    df = pd.read_csv(data_files.BACKGROUND_SURVEY_DATA)
    df = df.drop(df.columns[1:13], axis=1).drop(df.columns[14:19], axis=1).dropna()
    questions = list(df.columns)[1]
    new_columns = get_columns(questions)

    row_index = 1
    for row in df.itertuples():
        answers = row[2].split(",")
        column_index = 0
        for column in new_columns:
            if column_index < len(answers):
                df.at[row_index, column] = map_to_number(answers[column_index])
            column_index += 1
        row_index += 1
    df.drop(df.columns[1], axis=1)
    return df


# Exports the processed dataframe into a csv.
def export_to_csv(df):
    """
    Exports the processed dataframe into a csv.
    :param df: The df to export.
    """
    output_dir = os.path.join(data_files.OUTPUT_DIRECTORY, "processed_background_survey" + '.csv')
    df.to_csv(output_dir, index=False)


def get_columns(questions):
    """
    This separates the questions into a list so they can be used to update the columns in the dataframe.
    :param questions: a string of the questions to process.
    """
    new_columns = []
    for question in questions.splitlines():
        substring = re.search(r"\[(.*?)]", question)
        if substring:
            new_columns.append(substring.group(1).replace("_", " "))
    return new_columns


def map_to_number(answer):
    """
    Map a number to the student's answer.
    :param answer: the answer to map.
    """
    if answer == "Strongly Disagree":
        return -2
    elif answer == "Disagree":
        return -1
    elif answer == "Neither Agree Nor Disagree":
        return 0
    elif answer == "Agree":
        return 1
    elif answer == "Strongly Agree":
        return 2
    else:
        return 0


if __name__ == "__main__":
    data = prepare_df()
    export_to_csv(data)
