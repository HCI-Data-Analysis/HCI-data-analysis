import datetime
import json
import os

from canvasapi import Canvas


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def canvas_submission_retrieval(course_id, access_token, export_dir):
    canvas = Canvas('https://canvas.ubc.ca', access_token)
    assignments = canvas.get_course(course_id).get_assignments()
    for assignment in assignments:
        submissions = assignment.get_submissions()
        filename = str(course_id) + "_" + str(assignment.id)
        output_dir = os.path.join(export_dir, filename + '.json')
        with open(output_dir, "w") as f:
            json_submissions = []
            for submission in submissions:
                submission_dict = submission.__dict__
                submission_dict.pop('_requester')
                json_submissions.append(json.dumps(submission_dict, indent=4, cls=DateTimeEncoder))
            f.write('[' + ','.join(json_submissions) + ']')

