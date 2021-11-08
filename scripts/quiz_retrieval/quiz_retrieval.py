import json
import os

from api import CanvasAPI
from util import setup_submissions_filepath, get_quiz_id_from_file_name, DateTimeEncoder


def quiz_object_retrieval(output_dir):
    """
    Retrieve all quiz objects as .json files from the course and download all quizzes into
        "data/api/canvas/quiz_objects"
    Quiz object name will follow the format "quiz_object_[quiz_id].json"
    :return:
    """
    canvas_api = CanvasAPI()
    quizzes = canvas_api.get_quizzes()
    for quiz in quizzes:
        output_path = setup_submissions_filepath(quiz, output_dir, "quiz_objects", "quiz_object")
        download_quiz(quiz, output_path)


def download_quiz(quiz, output_filepath):
    """
    Download the given quiz object in to the specified output path
    :param quiz: quiz object
    :param output_filepath: a string containing the output path and name of the quiz object.
    :return:
    """
    with open(output_filepath, 'w') as f:
        json_quiz = []
        quiz_dict = quiz.__dict__
        quiz_dict.pop('_requester')
        json_quiz.append(json.dumps(quiz_dict, indent=4, cls=DateTimeEncoder))
        f.write('[' + ','.join(json_quiz) + ']')


def get_quiz_name(quiz_id, quiz_object_path):
    """
    Return the name of the quiz as a string giving the quiz_id
    :param quiz_object_path: a string containing the directory of where the quiz objects are stored
    :param quiz_id: A string that contains the quiz_id
    :return: A string that contains the name of the quiz
    """
    full_path = os.path.join(quiz_object_path, "quiz_objects")
    for quiz_object in os.listdir(full_path):
        if quiz_object.endswith('.json'):
            file_quiz_id = get_quiz_id_from_file_name(quiz_object)

            if file_quiz_id == quiz_id:
                quiz_object_path = os.path.join(full_path, quiz_object)
                with open(quiz_object_path, 'r') as f:
                    file = f.read()
                    json_file = json.loads(file)
                    if json_file:
                        return json_file[0]['title']
                    else:
                        return quiz_id + " can't retrieve quiz name"


def get_quiz_object(quiz_id, quiz_object_path):
    """
    Returns the path of the quiz object with the corresponding quiz_id
    :param quiz_object_path: a string containing the directory of where the quiz objects are stored
    :param quiz_id: a string containing the quiz id
    :return: the path of the quiz object with the corresponding quiz_id
    """

    for quiz_object in os.listdir(quiz_object_path):

        if quiz_object.endswith('.json'):
            file_quiz_id = get_quiz_id_from_file_name(quiz_object)
            if file_quiz_id == quiz_id:
                quiz_object_path = os.path.join(quiz_object_path, quiz_object)
                return quiz_object_path
            else:
                continue
        else:
            continue
