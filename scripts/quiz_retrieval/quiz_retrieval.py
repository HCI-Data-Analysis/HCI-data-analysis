import datetime
import json
import os

from api import CanvasAPI
from scripts import setup_submissions_filepath
from util import  mkdir_if_not_exists

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


def get_quiz_name(quiz_id):
    """
    Return the name of the quiz as a string giving the quiz_object.json file
    :param file_dir: A string that contains the directory which the quiz_object.json file is in
    :param file_name: A string that contains the name of the quiz_object.json file
    :return: A string that contains the name of the quiz
    """
    full_path = os.path.join(OUTPUT_DIR, "quiz_objects")
    for quiz_object in os.listdir(full_path):
        if quiz_object.endswith('.json'):
            file_quiz_id = quiz_object[12:18]  # the course id is the 12th to 18th character in the file name

            if file_quiz_id == quiz_id:
                quiz_object_path = os.path.join(full_path, quiz_object)
                with open(quiz_object_path, 'r') as f:
                    file = f.read()
                    json_file = json.loads(file)
                    if json_file:
                        return json_file[0]['title']
                    else:
                        return quiz_id + " can't retrieve quiz name"


def get_quiz_object(quiz_id):
    """
    Returns the path of the quiz object with the corresponding quiz_id
    :param quiz_id: a string containing the quiz id
    :return:the path of the quiz object with the corresponding quiz_id
    """
    full_path = os.path.join(OUTPUT_DIR, "quiz_objects")
    for quiz_object in os.listdir(full_path):

        if quiz_object.endswith('.json'):
            file_quiz_id = quiz_object[12:18]  # the course id is the 12th to 18th character in the file name
            if file_quiz_id == quiz_id:
                quiz_object_path = os.path.join(full_path, quiz_object)
                return quiz_object_path
            else:
                continue


if __name__ == '__main__':
    quiz_object_retrieval()

    file_dir = os.path.join(OUTPUT_DIR, "quiz_objects")
    # for file in os.listdir(file_dir):
    #     if file.endswith('.json'):
    #         print(get_quiz_name(file_dir, file))
