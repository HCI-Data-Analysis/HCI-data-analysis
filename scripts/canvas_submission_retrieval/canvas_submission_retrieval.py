import datetime
import json
import os

from api import CanvasAPI, get_default_course_id
from util import Encoder, mkdir_if_not_exists


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)
        

SUBMISSION_REMOVE_VALUES = {
    'assignment': ['preview_url'],
    'quiz': ['html_url', 'result_url', 'validation_token'],
}


def canvas_submission_retrieval(export_dir, encoder: Encoder, course_id=None):
    canvas_api = CanvasAPI()
    assignments = canvas_api.get_assignments_from_course(course_id)

    course_id = course_id or get_default_course_id()
    mkdir_if_not_exists(os.path.join(export_dir, course_id))

    temp_ta = {}
    download_submission(assignments, temp_ta, export_dir, course_id, encoder, 'assignment')
    quizzes = canvas.get_course(course_id).get_quizzes()
    download_submission(quizzes, temp_ta, export_dir, course_id, encoder, 'quiz')


def download_submission(submission_parent, ta_dict, export_dir, course_id, encoder, submission_type):
    for index, parent_type in enumerate(submission_parent, start=1):
        submissions = parent_type.get_submissions()
        filename = submission_type + "_" + str(index) + "_" + str(parent_type.id)
        output_dir = os.path.join(export_dir, course_id, filename + '.json')
        with open(output_dir, "w") as f:
            json_submissions = []
            for submission in submissions:
                submission_dict = submission.__dict__
                submission_dict.pop('_requester')
                for key in SUBMISSION_REMOVE_VALUES[submission_type]:
                    submission_dict.pop(key)
                if submission_dict.get('grader_id', None):
                    submission_dict['grader_id'] = ta_dict.setdefault(submission_dict['grader_id'], len(ta_dict) + 1)
                submission_dict['user_id'] = encoder.encode(canvas_id=submission_dict['user_id'])
                json_submissions.append(json.dumps(submission_dict, indent=4, cls=DateTimeEncoder))
            f.write('[' + ','.join(json_submissions) + ']')
