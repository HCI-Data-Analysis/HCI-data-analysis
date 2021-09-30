import os

from api import get_default_course_id
from scripts import canvas_submission_retrieval, generate_key
import sys

from util import Encoder

KEY_PATH = 'keys/Key.csv'
EXPORT_DIR = 'data/canvas_submission'

if __name__ == '__main__':

    encoder = Encoder(KEY_PATH)

    # os.mkdir(EXPORT_DIR)
    try:
        canvas_course_id = sys.argv[1]
    except IndexError:
        canvas_course_id = get_default_course_id()

    os.mkdir(os.path.join(EXPORT_DIR, canvas_course_id))
    canvas_submission_retrieval(EXPORT_DIR, encoder, canvas_course_id)
