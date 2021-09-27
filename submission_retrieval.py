from scripts import canvas_submission_retrieval
import sys

EXPORT_DIR = 'data/canvas_submission'
CANVAS_ACCESS_TOKEN = sys.argv[1]
CANVAS_COURSE_ID = sys.argv[2]

if __name__ == '__main__':
    # submission retrieval
    canvas_submission_retrieval(CANVAS_COURSE_ID, CANVAS_ACCESS_TOKEN, EXPORT_DIR)
