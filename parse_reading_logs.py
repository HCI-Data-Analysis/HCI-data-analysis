from scripts import parse_reading_logs_all
from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH

READING_LOG_PATH = "data/api/canvas/reading_logs"

if __name__ == "__main__":
    parse_reading_logs_all(READING_LOG_PATH, MODULE_PARAGRAPHS_OUTPUT_FILEPATH)
