import datetime
import json
import sys

from canvasapi import Canvas


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def canvas_submission_retrieval(course_id, access_token):
    canvas = Canvas('https://canvas.ubc.ca', access_token)
    assignments = canvas.get_course(course_id).get_assignments()
    for assignment in assignments:
        submissions = assignment.get_submissions()
        with open(f"../../data/{course_id}_{assignment.id}.json", "w") as f:
            json_submissions = []
            for submission in submissions:
                submission_dict = submission.__dict__
                submission_dict.pop('_requester')
                json_submissions.append(json.dumps(submission_dict, indent=4, cls=DateTimeEncoder))
            f.write('[' + ','.join(json_submissions) + ']')


if __name__ == '__main__':
    canvas_access_token = sys.argv[1]
    canvas_course_id = sys.argv[2]
    canvas_submission_retrieval(canvas_course_id, canvas_access_token)
