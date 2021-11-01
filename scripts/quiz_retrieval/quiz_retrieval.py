import datetime
import json
import os

from api import CanvasAPI, get_default_course_id
from scripts import setup_submissions_filepath


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def quiz_name_retrieval(course_id):
    canvas_api = CanvasAPI()
    course_id = course_id or get_default_course_id()
    # course_submissions_dir = mkdir_if_not_exists(os.path.join(export_dir, course_id))
    output_dir = "data/api/canvas"
    quizzes = canvas_api.get_quizzes()
    for quiz in quizzes:

        output_path = setup_submissions_filepath(quiz, output_dir, "quiz_objects", "quiz_object" )
        download_quiz(quiz, output_path)


def download_quiz(quiz, output_filepath):
    with open(output_filepath, 'w') as f:
        json_quiz = []
        quiz_dict = quiz.__dict__
        quiz_dict.pop('_requester')
        json_quiz.append(json.dumps(quiz_dict, indent=4, cls=DateTimeEncoder))
        f.write('[' + ','.join(json_quiz) + ']')


if __name__ == '__main__':
    quiz_name_retrieval(74915)
