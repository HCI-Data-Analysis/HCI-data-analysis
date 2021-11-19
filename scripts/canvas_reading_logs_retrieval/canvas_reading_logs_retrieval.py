import os
import ssl

from api import CanvasAPI, get_default_course_id
from util import Encoder, mkdir_if_not_exists
from urllib.request import urlopen

SUBMISSION_TYPE = 'online_upload'


def canvas_reading_logs_retrieval(export_dir, encoder: Encoder, course_id=None, assignment_id=None):
    """
    Downloads reading logs.
    :param export_dir: the container directory to store all submission data within
    :param encoder: encoder instance used to encode student ids into random ids
    :param course_id: the course id to download submissions for (defaults to the course id set in .env)
    """
    canvas_api = CanvasAPI()
    course_id = course_id or get_default_course_id()
    course_reading_logs_dir = mkdir_if_not_exists(os.path.join(export_dir, course_id))

    assignment = canvas_api.get_assignment(course_id)

    output_path = setup_reading_logs_filepath(course_reading_logs_dir, 'reading_logs')
    assignment_submissions = assignment.get_submissions()
    download_reading_logs(assignment_submissions, output_path, encoder)


def setup_reading_logs_filepath(parent_dir: str, sub_dir: str) -> str:
    """
    Get the correct filepath for a reading logs download
    :param parent_dir: the parent directory path
    :param sub_dir: the name of the sub directory for this object type's submissions to be saved
    :param assignment: the assignment we are retrieving the reading logs for
    :return: a string filepath
    """
    output_path = os.path.join(parent_dir, sub_dir)
    mkdir_if_not_exists(output_path)
    return output_path


def download_reading_logs(submissions, output_filepath: str, encoder: Encoder):
    """
    Downloads and unzips reading logs for an assignment.
    :param submissions: submissions objects to be downloaded
    :param output_filepath: the filepath for this data to be saved in
    :param encoder: encoder instance used to encode student ids into random ids
    """
    context = ssl.SSLContext()
    for submission in submissions:
        submission_dict = submission.__dict__
        if submission_dict['submission_type'] == SUBMISSION_TYPE:
            output = os.path.join(output_filepath, str(submission_dict['assignment_id']),
                                  str(encoder.encode(canvas_id=submission_dict['user_id'])))
            mkdir_if_not_exists(output, True)
            for attachment in submission_dict['attachments']:
                submission_url = attachment.get('url', None)
                ssl._create_default_https_context = ssl.create_default_context()
                with urlopen(submission_url, context=context) as file:
                    file_name = file.headers.get_filename()
                    with open(os.path.join(output, file_name), 'wb') as f:
                        f.write(file.read())
