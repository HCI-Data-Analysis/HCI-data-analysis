import os

from scripts import survey_anonymize
from util import Encoder, mkdir_if_not_exists, KEY_PATH

EXPORT_DIR = 'data/anonymized'

module_feedback_survey_paths = [
    'raw_data/341_Background_Survey_Header.csv'
]

# THIS IS A TEMP FILE This anonymizing process will be placed into anonymize.py, but for the simplicity of Dr. Hui
# running this script, it has been created as a separate file

if __name__ == '__main__':
    mkdir_if_not_exists(EXPORT_DIR)
    encoder = Encoder(KEY_PATH)

    for feedback_survey_path in module_feedback_survey_paths:
        file_name = os.path.basename(feedback_survey_path)
        survey_anonymize(feedback_survey_path, EXPORT_DIR, file_name, encoder)
