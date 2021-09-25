import pandas as pd

from scripts.convert_gradebook.convert_gradebook import convert_grade_book
from scripts.convert_survey.convert_survey import convert_survey
from scripts.convert_ta_survey.convert_ta_survey import convert_ta_survey
from scripts.convert_zip_file.convert_zip_file_id import convert_zip_file
from util import Encoder

KEY_PATH = './keys/Key.csv'

BACKGROUND_SURVEY_PATH = 'raw_data/341_Background_Survey_Header.csv'
BACKGROUND_EXPORT_PATH = 'data/background_survey.csv'
GRADE_BOOK_CSV_PATH = 'raw_data/2021-09-13T1128_Grades-COSC_341_COSC_541_101_2020W.csv'
GRADE_BOOK_EXPORT_PATH = 'data/grade_book.csv'
IMPRESSION_SURVEY_PATH = 'raw_data/Your_Impression_of_HCI__10_min_Header-First.csv'
IMPRESSION_EXPORT_PATH = 'data/impression_survey.csv'
IMPRESSION_SURVEY_PATH_2 = 'raw_data/Your_Impression_of_HCI__10_min_Header-Second.csv'
IMPRESSION_EXPORT_PATH_2 = 'data/impression_survey_2.csv'
TA_SURVEY_PATH = 'raw_data/341_TA_resources_survey_W2020T2_September_13_2021_12.36.csv'
TA_EXPORT_PATH = 'data/ta_survey.csv'

if __name__ == '__main__':
    encoder = Encoder(KEY_PATH)
    # Convert Impression Survey
    survey = convert_survey(pd.read_csv(IMPRESSION_SURVEY_PATH), encoder)
    survey.to_csv(IMPRESSION_EXPORT_PATH, index=False)

    # Convert Impression Survey 2
    survey = convert_survey(pd.read_csv(IMPRESSION_SURVEY_PATH_2), encoder)
    survey.to_csv(IMPRESSION_EXPORT_PATH_2, index=False)

    # Convert Background Survey
    survey = convert_survey(pd.read_csv(BACKGROUND_SURVEY_PATH), encoder)
    survey.to_csv(BACKGROUND_EXPORT_PATH, index=False)

    # Convert TA Survey
    survey = convert_ta_survey(pd.read_csv(TA_SURVEY_PATH), encoder)
    survey.to_csv(TA_EXPORT_PATH, index=False)

    # Convert GradeBook
    survey = convert_grade_book(pd.read_csv(GRADE_BOOK_CSV_PATH), encoder)
    survey.to_csv(GRADE_BOOK_EXPORT_PATH, index=False)

    # # TODO: Resolve path input procedure
    # # convert_zip_file()
