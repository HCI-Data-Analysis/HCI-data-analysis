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


def canvas_submission_retrieval(course_id, access_token, export_dir, encoder: Encoder):
    canvas = Canvas('https://canvas.ubc.ca', access_token)
    assignments = canvas.get_course(course_id).get_assignments()
    temp_ta = {}
    for index, assignment in enumerate(assignments, start=1):
        submissions = assignment.get_submissions()
        filename = str(index) + "_" + str(assignment.id)
        output_dir = os.path.join(export_dir, course_id, filename + '.json')
        with open(output_dir, "w") as f:
            json_submissions = []
            for submission in submissions:
                submission_dict = submission.__dict__
                for key in ['_requester', 'preview_url', 'course_id']:
                    submission_dict.pop(key)
                submission_dict['grader_id'] = temp_ta.setdefault(submission_dict['grader_id'], len(temp_ta) + 1)
                submission_dict['user_id'] = encoder.encode(canvas_id=submission_dict['user_id'])
                json_submissions.append(json.dumps(submission_dict, indent=4, cls=DateTimeEncoder))
            f.write('[' + ','.join(json_submissions) + ']')

