from api import CanvasAPI, get_default_course_id
from util import mkdir_if_not_exists
import os

def quiz_retrieval(export_dir, course_id):
    canvas_api = CanvasAPI()
    course_id = course_id or get_default_course_id()
    course_submissions_dir = mkdir_if_not_exists(os.path.join(export_dir, course_id))