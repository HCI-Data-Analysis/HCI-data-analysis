import os

import numpy as np
import pandas as pd

from schemas import KeySchema
from schemas.surveys import SurveySchema
from util.encoder import Encoder


def survey_anonymize(survey_path, output_dir, filename, encoder: Encoder):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized survey specified in
    <survey_filepath>, using the keys file located in <keys_filepath>

    :param survey_path: A string containing the path of the survey to be anonymized
    :param output_dir: A string containing the path of the directory where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param encoder: Instance of the encoder model that has been initialized with
    """
    survey = pd.read_csv(survey_path)

    survey[KeySchema.DATA448_ID] = survey.apply(lambda row: encoder.encode(row[SurveySchema.CANVAS_ID]))

    survey = survey.drop(columns=[SurveySchema.STUDENT_NAME, SurveySchema.CANVAS_ID, SurveySchema.SECTION_ID,
                                  SurveySchema.SECTION])

    survey = survey.set_index(KeySchema.DATA448_ID)

    output_dir = os.path.join(output_dir, filename + ".csv")

    survey.to_csv(output_dir)
