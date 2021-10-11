import os

import pandas as pd

from schemas import KeySchema, RawSurveySchema
from util.encoder import Encoder


def survey_anonymize(survey_path, output_dir, filename, encoder: Encoder):
    """
    Outputs a file to called <filename> to <output_filepath> that contains the anonymized survey specified in
    <survey_filepath>, using the keys file located in <keys_filepath>

    :param survey_path: A string containing the path of the survey to be anonymized
    :param output_dir: A string containing the path of the directory where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param encoder: Instance of the encoder model that has been initialized with
    """
    survey = pd.read_csv(survey_path)
    survey = survey.rename(columns={RawSurveySchema.CANVAS_ID: KeySchema.DATA448_ID})

    survey[KeySchema.DATA448_ID] = survey[KeySchema.DATA448_ID].map(
        lambda canvas_id: encoder.encode(canvas_id=canvas_id)
    )

    if RawSurveySchema.BACKGROUND_SV_FRIENDS in survey:
        survey[RawSurveySchema.BACKGROUND_SV_FRIENDS] = survey[RawSurveySchema.BACKGROUND_SV_FRIENDS].map(
            lambda student_names: encode_student_names_string(student_names, encoder)
        )

    survey = survey.drop(columns=[RawSurveySchema.STUDENT_NAME])

    output_dir = os.path.join(output_dir, filename + ".csv")
    survey.to_csv(output_dir, index=False)


def encode_student_names_string(student_names: str, encoder: Encoder):
    sn_split = student_names.split(', ')
    sn_every_other_comma = list(map(', '.join, zip(sn_split[::2], sn_split[1::2])))
    return map(lambda student_name: encoder.encode(student_name=student_name), sn_every_other_comma)
