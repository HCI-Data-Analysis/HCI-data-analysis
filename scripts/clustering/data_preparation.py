import pandas as pd
import os
import re
from schemas import data_files


def prepare_data_HCI(survey_path, schema_path, output_dir):
    """
    Convert all the ordinal responses in <survey_path> to corresponding numerical representations. (Including flipping the negative
    questions response)
    Calculate the average rating each student give for each category
    Outputs a file to <output_path> containing the above information
    :param survey_path: A string containing the filepath of the survey being prepared
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :param output_dir: A string containing the path where the anonymized file should be placed
    """

    survey = pd.read_csv(survey_path)
    schema = pd.read_csv(schema_path)

    survey = map_to_number(survey)
    convert_negative(survey, schema)
    average_score(survey, schema)

    export_to_csv(survey, output_dir)


# Prepares and cleans the dataframe so it is possible to use it for clustering.
def prepare_data_background(survey_path, schema_path, output_dir):
    df = pd.read_csv(survey_path)
    schema = pd.read_csv(schema_path)

    convert_negative(df, schema)
    average_score(df, schema)

    export_to_csv(df, output_dir)


# This separates the questions into a list so they can be used to update the columns in the dataframe.
def get_columns(questions):
    new_columns = []
    for question in questions.splitlines():
        substring = re.search(r"\[(.*?)]", question)
        if substring:
            new_columns.append(substring.group(1).replace("_", " "))
    return new_columns


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


def convert_negative(survey, schema):
    """
    Flip the response of negatively phrased question
    :param survey: a dataframe containing survey result
    :param schema: a dataframe containing the survey schema
    """
    negatives_col_nums = schema["col num 1"][schema["positive/negative"] < 1]
    for col in survey.iloc[:, negatives_col_nums]:
        survey[col] = survey[col].apply(lambda x: x * -1)


def average_score(survey, schema):
    """
    Compute the average score for each category
    :param survey: a dataframe containing survey result
    :param schema: a dataframe containing the survey schema
    :return:
    """

    categories = schema["category"].unique()
    for category in categories:
        questions = schema[schema["category"] == category]
        question_col_num = questions["col num 1"]
        question_df = survey.iloc[:, question_col_num]
        survey[category] = question_df.sum(axis=1) / len(question_col_num)


def export_to_csv(df, output_dir):
    df = df.drop(df.columns[1], axis=1)

    student_info = df.iloc[:, 0]
    aggregate = df.iloc[:, -5:]
    result = pd.concat([student_info.reset_index(drop=True), aggregate.reset_index(drop=True)], axis=1)

    output_dir = os.path.join(data_files.OUTPUT_DIRECTORY, "for_clustering_" + data_files.FILE_NAME + '.csv')
    result.to_csv(output_dir, index=False)


if __name__ == '__main__':
    prepare_data_background(data_files.BACKGROUND_SURVEY_DATA, schema_path=data_files.BACKGROUND_SURVEY_SCHEMA,
                            output_dir=data_files.OUTPUT_DIRECTORY)
    # prepare_data_HCI(HCI_SURVEY_DATA,HCI_SURVEY_SCHEMA,OUTPUT_DIRECTORY)
