import os
import datetime
import json

from util import mkdir_if_not_exists


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


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)