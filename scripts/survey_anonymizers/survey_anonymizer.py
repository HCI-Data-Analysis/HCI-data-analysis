import os

import numpy as np
import pandas as pd


def survey_anonymize(survey_filepath, output_path, filename, keys_filepath):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized survey specified in
    <survey_filepath>, using the keys file located in <keys_filepath>

    :param survey_filepath: A string containing the filepath of the survey to be anonymized
    :param output_path: A string containing the path where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param keys_filepath: A string containing the filepath of the keys file containing all of the DATA448 IDs
    """
    survey = pd.read_csv(survey_filepath)
    keys = pd.read_csv(keys_filepath)

    survey['data448id'] = np.where(survey.id == keys.id, keys.data448id, 0)

    survey = survey.drop(['name', 'id'], axis=1)

    survey = survey.set_index('data448id')

    output_path = os.path.join(output_path, filename + ".csv")

    survey.to_csv(output_path)

#
# from pandas import DataFrame
# from util import Encoder, EncoderException
# from schemas import SurveySchema
#
#
# def convert_survey(survey_df: DataFrame, encoder: Encoder) -> DataFrame:
#     converted_survey_df = survey_df.drop(columns=[SurveySchema.NAME])
#     for i, row in converted_survey_df.iterrows():
#         try:
#             student_id = encoder.encode(canvas_id=row[SurveySchema.ID])
#             converted_survey_df.at[i, SurveySchema.ID] = student_id
#         except EncoderException:
#             converted_survey_df.drop(i, inplace=True)
#     return converted_survey_df
