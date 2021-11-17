import sys

from api import get_default_course_id
from scripts.canvas_reading_logs_retrieval import canvas_reading_logs_retrieval
from util import Encoder, KEY_PATH, mkdir_if_not_exists

EXPORT_DIR = 'data/canvas_submission'

encoder = Encoder(KEY_PATH)

mkdir_if_not_exists(EXPORT_DIR)
try:
    canvas_course_id = sys.argv[1]
except IndexError:
    canvas_course_id = get_default_course_id()

canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id)
