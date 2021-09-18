import os
import numpy as np
import pandas as pd


def bg_anonymize(survey_filepath, output_path, filename, keys_filepath):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized background_survey specified in <survey_filepath>,
    using the keys file located in <keys_filepath>

    :param survey_filepath: A string containing the filepath of the background survey
    :param output_path: A string containing the path where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param keys_filepath: A string containing the filepath of the keys file containing all of the DATA448 IDs
    """
    bg_survey = pd.read_csv(survey_filepath)
    keys = pd.read_csv(keys_filepath)

    bg_survey['data448id'] = np.where(bg_survey.id == keys.id, keys.data448id, 0)

    bg_survey = bg_survey.drop(['name', 'id'], axis=1)

    bg_survey = bg_survey.set_index('data448id')

    output_path = os.path.join(output_path, filename + ".csv")

    bg_survey.to_csv(output_path)

    print(bg_survey)

# bg_anonymize('data/341_Background_Survey_Header.csv', 'data', 'anonymized_bg_survey', 'keys/keys.csv')
