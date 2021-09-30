from scripts import generate_key, gradebook_anonymize, survey_anonymize, anonymize_ta_survey
from util import Encoder, mkdir_if_not_exists

KEY_DIR = 'keys'
KEY_EXPORT_FILENAME = 'Key'

EXPORT_DIR = 'data/anonymized'
BACKGROUND_SURVEY_PATH = 'raw_data/341_Background_Survey_Header.csv'
BACKGROUND_EXPORT_FILENAME = 'background_survey'
GRADE_BOOK_CSV_PATH = 'raw_data/2021-09-13T1128_Grades-COSC_341_COSC_541_101_2020W.csv'
GRADE_BOOK_EXPORT_FILENAME = 'grade_book'
IMPRESSION_SURVEY_PATH = 'raw_data/Your_Impression_of_HCI__10_min_Header-First.csv'
IMPRESSION_EXPORT_FILENAME = 'impression_survey1'
IMPRESSION_SURVEY_PATH_2 = 'raw_data/Your_Impression_of_HCI__10_min_Header-Second.csv'
IMPRESSION_EXPORT_FILENAME_2 = 'impression_survey2'
TA_SURVEY_PATH = 'raw_data/341_TA_resources_survey_W2020T2_September_13_2021_12.36.csv'
TA_EXPORT_FILENAME = 'ta_survey'

if __name__ == '__main__':
    mkdir_if_not_exists('data/anonymized')
    # Generate Key file
    key_path = generate_key(GRADE_BOOK_CSV_PATH, KEY_DIR, KEY_EXPORT_FILENAME)
    encoder = Encoder(key_path)

    # Convert GradeBook
    gradebook_anonymize(GRADE_BOOK_CSV_PATH, EXPORT_DIR, GRADE_BOOK_EXPORT_FILENAME, encoder)

    # Convert BG Survey
    survey_anonymize(BACKGROUND_SURVEY_PATH, EXPORT_DIR, BACKGROUND_EXPORT_FILENAME, encoder)

    # Convert Impressions Survey #1
    survey_anonymize(IMPRESSION_SURVEY_PATH, EXPORT_DIR, IMPRESSION_EXPORT_FILENAME, encoder)

    # Convert Impressions Survey #2
    survey_anonymize(IMPRESSION_SURVEY_PATH_2, EXPORT_DIR, IMPRESSION_EXPORT_FILENAME_2, encoder)

    # Convert TA Survey
    anonymize_ta_survey(TA_SURVEY_PATH, EXPORT_DIR, TA_EXPORT_FILENAME, encoder)
