import os

from scripts import canvas_submission_retrieval, generate_key
import sys

from util import Encoder

KEY_PATH = 'keys/Key.csv'
EXPORT_DIR = 'data/canvas_submission'
CANVAS_ACCESS_TOKEN = sys.argv[1]
CANVAS_COURSE_ID = sys.argv[2]

if __name__ == '__main__':

    encoder = Encoder(KEY_PATH)

    os.mkdir(EXPORT_DIR)
    os.mkdir(os.path.join(EXPORT_DIR, CANVAS_COURSE_ID))

    canvas_submission_retrieval(CANVAS_COURSE_ID, CANVAS_ACCESS_TOKEN, EXPORT_DIR, encoder)
