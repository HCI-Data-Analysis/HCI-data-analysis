import pandas as pd
import os


def prepare_data(survey_path, schema_path, output_dir):
    '''
    Convert all the ordinal responses in <survey_path> to corresponding numerical representations. (Including flipping the negative
    questions response)
    Calculate the average rating each student give for each category
    Outputs a file to <output_path> containing the above information
    :param survey_path: A string containing the filepath of the survey being prepared
    :param schema_path: A string containing the file path of the schema document of the survey questions.
    :param output_dir: A string containing the path where the anonymized file should be placed
    '''

    # Convert ordinal values to numerical representations
    survey = pd.read_csv(survey_path)
    survey = survey.replace("Strongly Disagree", -2)
    survey = survey.replace("Disagree", -1)
    survey = survey.replace("Agree", 1)
    survey = survey.replace("Strongly Agree", 2)

    schema = pd.read_csv(schema_path)

    # Flip the response of negatively phrased question
    negatives_col_nums = schema["col num 1"][schema["positive/negative"] < 1]
    for col in survey.iloc[:, negatives_col_nums]:
        survey[col] = survey[col].apply(lambda x: x*-1)

    # Compute the average score for each category
    categories = schema["category"].unique()
    for category in categories:
        questions = schema[schema["category"] == category]
        question_col_num = questions["col num 1"]
        question_df = survey.iloc[:, question_col_num]
        survey[category] = question_df.sum(axis=1)/len(question_col_num)

    survey_name = os.path.basename(survey_path)

    student_info = survey.iloc[:, 0:5]
    aggregate = survey.iloc[:, -5:]

    result = pd.concat([student_info.reset_index(drop=True),aggregate.reset_index(drop=True)], axis=1)

    result.to_csv(output_dir+"/for_clustering_" + survey_name)


if __name__ == '__main__':
    prepare_data("../../../data/impression_survey1.csv", schema_path="../../../data/HCI_survey_schema.csv", output_dir="../../../data")
