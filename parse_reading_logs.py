import os

import dill

from scripts import parse_reading_logs_all, parse_reading_logs_module
from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH, CACHE_FOLDER, mkdir_if_not_exists

READING_LOG_PATH = "data/api/canvas/reading_logs"

if __name__ == "__main__":
    reading_durations_dict, content_quiz_performance_dict = parse_reading_logs_all(
        READING_LOG_PATH,
        MODULE_PARAGRAPHS_OUTPUT_FILEPATH
    )
    mkdir_if_not_exists(CACHE_FOLDER)

    with open(os.path.join(CACHE_FOLDER, 'reading_durations_dict.pkl'), 'wb') as f:
        dill.dump(reading_durations_dict, f)
    with open(os.path.join(CACHE_FOLDER, 'content_quiz_performance_dict.pkl'), 'wb') as f:
        dill.dump(content_quiz_performance_dict, f)
