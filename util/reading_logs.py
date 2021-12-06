import json
import os

import dill

from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH, normalize, CACHE_FOLDER


class ReadingLogsData:
    READING_LOG_PATH = "data/api/canvas/reading_logs_extras"

    module_paragraphs_dict = None
    reading_duration_dict = None
    content_quiz_performance_dict = None

    def get_module_paragraphs_dict(self) -> dict:
        if self.module_paragraphs_dict:
            return self.module_paragraphs_dict

        try:
            f = open(MODULE_PARAGRAPHS_OUTPUT_FILEPATH, mode='r')
        except FileNotFoundError as e:
            raise FileNotFoundError(f'{e}\nRun "python parse_module_paragraphs.py" first.')

        module_paragraphs = json.load(f)
        self.module_paragraphs_dict = module_paragraphs
        return module_paragraphs

    def get_parsed_reading_log_data(self) -> (dict, dict):
        if not self.reading_duration_dict and not self.content_quiz_performance_dict:
            try:
                with open(os.path.join(CACHE_FOLDER, 'reading_durations_dict.pkl'), 'rb') as f:
                    self.reading_duration_dict = dill.load(f)
                with open(os.path.join(CACHE_FOLDER, 'content_quiz_performance_dict.pkl'), 'rb') as f:
                    self.content_quiz_performance_dict = dill.load(f)
            except FileNotFoundError as e:
                raise FileNotFoundError(f'{e}\nRun "python parse_reading_logs.py" first.')

        return self.reading_duration_dict, self.content_quiz_performance_dict

    def page_reading_speed(self, module_num: int, page_num: int, data448_id: int = None,
                           adjust_for_difficulty: bool = None) -> float:
        """
        Retrieves the reading speed for a page. If given a data448_id, only retrieves that student's reading speed
        for the page. Without a data448_id, retrieves the average reading speed of that page. If desired,
        this reading speed can be adjusted to factor in difficulty.

        :param module_num: The module number
        :param page_num: The page number
        :param data448_id: A student's Data 448 id
        :param adjust_for_difficulty: Whether or not to normalize this reading speed for difficulty
        :return: a float representing reading speed in word per minute (WPM)
        """
        paragraph_list = self.get_paragraph_list(module_num, page_num)

        num_words = len(' '.join(paragraph_list).split(' '))
        duration = self.page_reading_duration(module_num, page_num, data448_id)

        speed_wpm = num_words / duration

        if adjust_for_difficulty:
            difficulty = get_text_difficulty_index(module_num, page_num)
            norm_difficulty = normalize(difficulty, 0, 100)
            return speed_wpm / norm_difficulty

        return speed_wpm

    def module_reading_speed(self, module_num: int, data448_id: int = None,
                             adjust_for_difficulty: bool = None) -> float:
        """
        Retrieves the reading speed for a module. If given a data448_id, only retrieves that student's reading speed
        for the page. Without a data448_id, retrieves the average reading speed of that page. If desired,
        this reading speed can be adjusted to factor in difficulty. In all cases, the returned value is the average
        reading speed from all pages within the module

        :param module_num: The module number
        :param data448_id: A student's Data 448 id
        :param adjust_for_difficulty: Whether or not to normalize this reading speed for difficulty
        :return: a float representing reading speed in word per minute (WPM)
        """
        page_reading_speeds = []
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        for page_num in module_paragraphs_dict[str(module_num)].keys():
            return self.page_reading_speed(module_num, int(page_num), data448_id, adjust_for_difficulty)

        return sum(page_reading_speeds) / len(page_reading_speeds)

    def get_paragraph_list(self, module_num: int, page_num: int) -> [str]:
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        page_paragraphs = []
        for section_id, data in module_paragraphs_dict[str(module_num)][str(page_num)]['sections'].items():
            page_paragraphs += data['paragraphs']
        return page_paragraphs

    def get_num_pages_in_module(self, module_num: int) -> int:
        module_paragraphs = self.get_module_paragraphs_dict()
        return len(module_paragraphs[str(module_num)])

    def page_reading_duration(self, module_num: int, page_num: int, data448_id: int = None) -> float:
        """Returns the page reading duration in minutes. Average of all students unless given a data_448 id."""
        self.reading_duration_dict, _ = self.get_parsed_reading_log_data()

        # Retrieve the correct DataFrame for the requested page.
        reading_duration_df = self.reading_duration_dict[f'{module_num}-{page_num}']

        if data448_id:
            start_time = reading_duration_df['start_time'][f'{data448_id}']
            end_time = reading_duration_df['end_time'][f'{data448_id}']
            duration_ms = int(end_time - start_time)
            return ms_to_minutes(duration_ms)

        reading_duration_df['duration'] = reading_duration_df['end_time'] - reading_duration_df['start_time']
        return ms_to_minutes(reading_duration_df['duration'].mean())

    def module_reading_duration(self, module_num: int, data448_id: int = None) -> float:
        """Returns the module reading duration (average of all page reading durations) in minutes.
        Average of all students unless given a data_448 id. """

        num_pages = self.get_num_pages_in_module(module_num)
        page_durations = []

        for page_num in range(1, num_pages + 1):
            page_durations.append(self.page_reading_speed(module_num, page_num, data448_id))

        return sum(page_durations) / len(page_durations)


def is_reading_log_file(reading_log_file_name) -> bool:
    if not reading_log_file_name.endswith('.json'):
        return False
    if '(' in reading_log_file_name and ')' in reading_log_file_name:  # check for duplicate files
        return False

    reading_log_name_array = reading_log_file_name.split('-')
    # make sure the file is a reading_log
    if (reading_log_name_array[0] != "COSC341"):  #& (reading_log_name_array[3] != "Reading") & (reading_log_name_array[4] != "Logs"):
        return False

    return True


def ms_to_minutes(duration_ms: int):
    return duration_ms / 1000 / 60


def get_text_difficulty_index(module_num: int, page_num: int = None) -> float:
    # TODO: read the data stored about the difficulty of each module/page and return the correctly difficulty index
    return 1
