import os.path

import pandas as pd

from scripts.gradebook_anonymizers import gradebook_anonymizer
from scripts.key_generator import key_generator
from scripts.survey_anonymizers import survey_anonymizer
from util import Encoder

KEY_DIR = '.\\keys'
KEY_EXPORT_FILENAME = 'Key'
KEY_PATH = os.path.join(KEY_DIR, KEY_EXPORT_FILENAME + '.csv')

EXPORT_DIR = 'data'
BACKGROUND_SURVEY_PATH = 'raw_data/341_Background_Survey_Header.csv'
BACKGROUND_EXPORT_FILENAME = 'background_survey'
GRADE_BOOK_CSV_PATH = 'raw_data/2021-09-13T1128_Grades-COSC_341_COSC_541_101_2020W.csv'
GRADE_BOOK_EXPORT_FILENAME = 'grade_book'
IMPRESSION_SURVEY_PATH = 'raw_data/Your_Impression_of_HCI__10_min_Header-First.csv'
IMPRESSION_EXPORT_FILENAME = 'impression_survey'
IMPRESSION_SURVEY_PATH_2 = 'raw_data/Your_Impression_of_HCI__10_min_Header-Second.csv'
IMPRESSION_EXPORT_FILENAME_2 = 'impression_survey_2'
TA_SURVEY_PATH = 'raw_data/341_TA_resources_survey_W2020T2_September_13_2021_12.36.csv'
TA_EXPORT_FILENAME = 'ta_survey'

if __name__ == '__main__':
    # Generate Key file
    key_generator.generate_key(GRADE_BOOK_CSV_PATH, KEY_DIR, KEY_EXPORT_FILENAME)

    encoder = Encoder(KEY_PATH)

    # Convert GradeBook
    gradebook_anonymizer.gradebook_anonymize(GRADE_BOOK_CSV_PATH, EXPORT_DIR, GRADE_BOOK_EXPORT_FILENAME, encoder)

    # Convert BG Survey
    survey_anonymizer.survey_anonymize(BACKGROUND_SURVEY_PATH, EXPORT_DIR, BACKGROUND_EXPORT_FILENAME, encoder)
