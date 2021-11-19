import sys

from api import get_default_course_id
from scripts.canvas_reading_logs_retrieval import canvas_reading_logs_retrieval
from util import Encoder, KEY_PATH, mkdir_if_not_exists

EXPORT_DIR = 'data/canvas_submission'
ASSIGNMENT_IDS = [741711, 741731, 741733, 741741, 741741, 741743, 741742, 741742, 741750, 741751,
                  741752, 741753]

if __name__ == "__main__":
    encoder = Encoder(KEY_PATH)

    mkdir_if_not_exists(EXPORT_DIR)
    try:
        canvas_course_id = sys.argv[1]
    except IndexError:
        canvas_course_id = get_default_course_id()

    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[0])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[1])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[2])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[3])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[4])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[5])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[6])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[7])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[8])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[9])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[10])
    canvas_reading_logs_retrieval(EXPORT_DIR, encoder, canvas_course_id, ASSIGNMENT_IDS[11])
