import datetime
import json
import os

from api import CanvasAPI, get_default_course_id
from scripts import setup_submissions_filepath

OUTPUT_DIR = "../../data/api/canvas"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def quiz_object_retrieval():
    canvas_api = CanvasAPI()
    output_dir = OUTPUT_DIR
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


def get_quiz_name(file_dir, file_name):
    """
    Return the name of the quiz as a string giving the quiz_object.json file
    :param file_dir: A string that contains the directory which the quiz_object.json file is in
    :param file_name: A string that contains the name of the quiz_object.json file
    :return: A string that contains the name of the quiz
    """


if __name__ == '__main__':
   quiz_object_retrieval()
