import os
import re

from pandas import DataFrame


def clean_background_survey(survey_df: DataFrame, output):
    """
    Prepares and cleans the dataframe so it is possible to use it for clustering.
    Fixes the single column with all the questions in it.
    """
    survey_df = survey_df.drop(survey_df.columns[1:13], axis=1).drop(survey_df.columns[14:19], axis=1).dropna()
    questions = list(survey_df.columns)[1]
    new_columns = _get_columns(questions)

    row_index = 1
    for row in survey_df.itertuples():
        answers = row[2].split(",")
        column_index = 0
        for column in new_columns:
            if column_index < len(answers):
                survey_df.at[row_index, column] = answers[column_index]
            column_index += 1
        row_index += 1
    survey_df.drop(survey_df.columns[1], axis=1)
    output_dir = os.path.join(output, "processed_background_survey" + '.csv')
    survey_df.to_csv(output_dir, index=False)


def _get_columns(questions):
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
