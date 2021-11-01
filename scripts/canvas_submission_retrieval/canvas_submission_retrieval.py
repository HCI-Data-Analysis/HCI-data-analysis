import datetime
import json
import os

from api import CanvasAPI, get_default_course_id
from util import Encoder, mkdir_if_not_exists

ASSIGNMENT = 'assignment'
QUIZ = 'quiz'
REMOVE_VALUES = {
    ASSIGNMENT: ['preview_url'],
    QUIZ: ['html_url', 'result_url', 'validation_token'],
}


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def canvas_submission_retrieval(export_dir, encoder: Encoder, course_id=None):
    """
    Downloads assignment and quiz submission data.
    :param export_dir: the container directory to store all submission data (for assignments and quizzes) within
    :param encoder: encoder instance used to encode student ids into random ids
    :param course_id: the course id to download submissions for (defaults to the course id set in .env)
    """
    canvas_api = CanvasAPI()
    course_id = course_id or get_default_course_id()
    course_submissions_dir = mkdir_if_not_exists(os.path.join(export_dir, course_id))

    grader_id_key = {}
    assignments = canvas_api.get_assignments(course_id)
    quizzes = canvas_api.get_quizzes(course_id)

    for assignment in assignments:
        output_path = setup_submissions_filepath(assignment, course_submissions_dir, 'assignments', 'assignment')
        assignment_submissions = assignment.get_submissions()
        download_submissions(assignment_submissions, grader_id_key, output_path, encoder, REMOVE_VALUES[ASSIGNMENT])

    for quiz in quizzes:
        output_path = setup_submissions_filepath(quiz, course_submissions_dir, 'quizzes', 'quiz')
        quiz_submissions = quiz.get_submissions()
        download_submissions(quiz_submissions, grader_id_key, output_path, encoder, REMOVE_VALUES[QUIZ])


# Should I move this function to somewhere that is more like util for api?
def setup_submissions_filepath(obj, parent_dir: str, sub_dir: str, file_prefix: str) -> str:
    """
    Get the correct filepath for a submissions data download
    :param obj: the object (Assignment or Quiz) whose submissions we are saving
    :param parent_dir: the parent directory path
    :param sub_dir: the name of the sub directory for this object type's submissions to be saved
    :param file_prefix: a prefix to be prepended to the saved json file
    :return: a string filepath
    """
    mkdir_if_not_exists(os.path.join(parent_dir, sub_dir))
    output_path = os.path.join(parent_dir, sub_dir, f'{file_prefix}_{obj.id}.json')
    return output_path


def download_submissions(submissions, grader_id_key: dict, output_filepath: str, encoder: Encoder, removed_values=None):
    """
    Downloads anonymized submission data in JSON format to the specified output_filepath. Grader ids are replaced
    with incremental numbers in order of encounter.

    :param submissions: submissions objects to be downloaded
    :param grader_id_key: a dictionary mapping grader ids to incrementing numbers
    :param output_filepath: the filepath for this data to be saved in
    :param encoder: encoder instance used to encode student ids into random ids
    :param removed_values: a list containing the names of the fields to be removed from the saves JSON object altogether
    """
    removed_values = [] if not removed_values else removed_values
    with open(output_filepath, 'w') as f:
        json_submissions = []
        for submission in submissions:
            submission_dict = submission.__dict__
            submission_dict.pop('_requester')
            for key in removed_values:
                submission_dict.pop(key)
            if submission_dict.get('attachments', None):
                submission_dict.pop('attachments')
            if submission_dict.get('grader_id', None):
                submission_dict['grader_id'] = grader_id_key.setdefault(
                    submission_dict['grader_id'],
                    len(grader_id_key) + 1
                )
            submission_dict['user_id'] = encoder.encode(canvas_id=submission_dict['user_id'])
            json_submissions.append(json.dumps(submission_dict, indent=4, cls=DateTimeEncoder))
        f.write('[' + ','.join(json_submissions) + ']')
