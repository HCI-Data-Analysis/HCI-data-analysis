import datetime
import json
import os

from canvasapi import Canvas

from util import Encoder


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


def canvas_submission_retrieval(course_id, access_token, export_dir, encoder: Encoder):
    canvas = Canvas('https://canvas.ubc.ca', access_token)
    temp_ta = {}
    assignments = canvas.get_course(course_id).get_assignments()
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
