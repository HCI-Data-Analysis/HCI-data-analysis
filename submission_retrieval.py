import os

from scripts import canvas_submission_retrieval, generate_key
import sys

from util import Encoder

KEY_DIR = 'keys'
KEY_EXPORT_FILENAME = 'Key'

EXPORT_DIR = os.path.join('data', 'canvas_submission')
CANVAS_ACCESS_TOKEN = sys.argv[1]
CANVAS_COURSE_ID = sys.argv[2]
GRADE_BOOK_CSV_PATH = 'raw_data/2021-09-13T1128_Grades-COSC_341_COSC_541_101_2020W.csv'

if __name__ == '__main__':

    encoder = Encoder("keys/Key.csv")

    os.mkdir(EXPORT_DIR)
    os.mkdir(os.path.join(EXPORT_DIR, CANVAS_COURSE_ID))

    canvas_submission_retrieval(CANVAS_COURSE_ID, CANVAS_ACCESS_TOKEN, EXPORT_DIR, encoder)
