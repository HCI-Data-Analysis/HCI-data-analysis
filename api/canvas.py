from canvasapi import Canvas

CANVAS_BASE_URL = 'https://canvas.ubc.ca'
ACCESS_TOKEN = 'test'


class CanvasAPI:
    canvas_api = None

    def __init__(self):
        self.canvas_api = Canvas(CANVAS_BASE_URL, ACCESS_TOKEN)

    def get_assignments_from_course(self, course_id):
        return self.canvas_api.get_course(course_id).get_assignments()
