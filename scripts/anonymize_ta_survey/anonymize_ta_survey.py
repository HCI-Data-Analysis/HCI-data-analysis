import os

import pandas as pd

from schemas import RawTASurveySchema
from util import Encoder


def anonymize_ta_survey(ta_survey_path, output_dir, filename, encoder: Encoder):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized gradebook specified in
    <gradebook_path>, using the keys file located in <keys_filepath>

    :param ta_survey_path: A string containing the filepath of the gradebook to be anonymized
    :param output_dir: A string containing the path where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param encoder: Instance of the encoder model that has been initialized with
    """

    file = pd.read_csv(ta_survey_path)

    file = file.drop(columns=[
        RawTASurveySchema.STATUS,
        RawTASurveySchema.IP_ADDRESS,
        RawTASurveySchema.RESPONSE_ID,
        RawTASurveySchema.RECIPIENT_FIRST_NAME,
        RawTASurveySchema.RECIPIENT_LAST_NAME,
        RawTASurveySchema.RECIPIENT_EMAIL,
        RawTASurveySchema.EXTERNAL_REFERENCE,
        RawTASurveySchema.LATITUDE,
        RawTASurveySchema.LONGITUDE,
        RawTASurveySchema.DISTRIBUTION_CHANNEL
    ]).drop(labels=[0, 1], axis=0)

    output_dir = os.path.join(output_dir, filename + '.csv')
    file.to_csv(output_dir, index=False)
