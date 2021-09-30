import os

from canvasapi import Canvas
from dotenv import load_dotenv

load_dotenv()

CANVAS_BASE_URL = 'https://canvas.ubc.ca'
ACCESS_TOKEN = os.getenv('CANVAS_ACCESS_TOKEN')


def get_default_course_id():
    return os.getenv('CANVAS_COURSE_ID')


class CanvasAPI:
    canvas_api = None

    def __init__(self):
        self.canvas_api = Canvas(CANVAS_BASE_URL, ACCESS_TOKEN)

    def get_assignments_from_course(self, course_id=None):
        if not course_id:
            course_id = get_default_course_id()
        return self.canvas_api.get_course(course_id).get_assignments()

    def get_quiz_submissions(self, course_id, quiz_id):
        pass

    def get_quiz(self, course_id, quiz_id):
        pass
