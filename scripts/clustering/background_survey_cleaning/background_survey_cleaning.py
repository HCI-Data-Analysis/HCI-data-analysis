import re
import pandas as pd
import os
from sklearn.cluster import KMeans

BACKGROUND_SURVEY_SCHEMA = "../../../data/background_survey_schema.csv"
BACKGROUND_SURVEY_DATA = "../../../data/background_survey.csv"
OUTPUT_DIRECTORY = "../../../data"
FILE_NAME = "processed_background_survey"


# Prepares and cleans the dataframe so it is possible to use it for clustering.
def prepare_df():
    df = pd.read_csv(BACKGROUND_SURVEY_DATA)
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
    return df


# Exports the processed dataframe into a csv.
def export_to_csv():
    df = prepare_df()
    df = df.drop(df.columns[1], axis=1)
    output_dir = os.path.join(OUTPUT_DIRECTORY, FILE_NAME + '.csv')
    df.to_csv(output_dir, index=False)


# This separates the questions into a list so they can be used to update the columns in the dataframe.
def get_columns(questions):
    new_columns = []
    for question in questions.splitlines():
        substring = re.search(r"\[(.*?)]", question)
        if substring:
            new_columns.append(substring.group(1).replace("_", " "))
    return new_columns


# Assign a number to the student's answer.
def map_to_number(answer):
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
    export_to_csv()