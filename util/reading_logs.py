import json
import os
import statistics

import dill

from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH, CACHE_FOLDER

START_TIME_KEY = 'start_time'
END_TIME_KEY = 'end_time'
DURATION_KEY = 'duration'


class ReadingLogsData:
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
        if not self.reading_duration_dict or not self.content_quiz_performance_dict:
            try:
                with open(os.path.join(CACHE_FOLDER, 'reading_durations_dict.pkl'), 'rb') as f:
                    self.reading_duration_dict = dill.load(f)
                with open(os.path.join(CACHE_FOLDER, 'content_quiz_performance_dict.pkl'), 'rb') as f:
                    self.content_quiz_performance_dict = dill.load(f)
            except FileNotFoundError as e:
                raise FileNotFoundError(f'{e}\nRun "python parse_reading_logs.py" first.')

        return self.reading_duration_dict, self.content_quiz_performance_dict

    def get_reading_duration_dict(self):
        return self.reading_duration_dict if self.reading_duration_dict else self.get_parsed_reading_log_data()[0]

    def get_content_quiz_performance_dict(self):
        return self.content_quiz_performance_dict if self.content_quiz_performance_dict else \
            self.get_parsed_reading_log_data()[1]

    def get_page_word_count(self, module_num: int, page_num: int) -> int:
        """
        Gets the word count for the page in a specified module.
        :param module_num: The module number.
        :param page_num: The page number.
        """
        paragraph_list = self.get_paragraph_list(module_num, page_num)
        return len(' '.join(paragraph_list).split(' '))

    def page_reading_speed(self, module_num: int, page_num: int, data448_id: int = None) -> (float, float):
        """
        Retrieves the reading speed for a page. If given a data448_id, only retrieves that student's reading speed
        for the page. Without a data448_id, retrieves the average reading speed of that page. If desired,
        this reading speed can be adjusted to factor in difficulty.

        Standard deviation is None if a data448_id is given

        :param module_num: The module number
        :param page_num: The page number
        :param data448_id: A student's Data 448 id
        :return: a float representing reading speed in word per minute (WPM), the standard deviation for this average
        """
        paragraph_list = self.get_paragraph_list(module_num, page_num)

        num_words = len(' '.join(paragraph_list).split(' '))

        if data448_id:
            page_reading_duration, _ = self.page_reading_duration(module_num, page_num, data448_id)
            page_reading_speed = num_words / page_reading_duration
            return page_reading_speed, None

        all_durations = self.page_reading_duration_list(module_num, page_num)
        student_reading_speeds = [(num_words / d) for d in all_durations]

        return mean_and_sd(student_reading_speeds)

    def module_reading_speed(self, module_num: int, data448_id: int = None) -> (float, float):
        """
        Retrieves the reading speed for a module. If given a data448_id, only retrieves that student's reading speed
        for the page. Without a data448_id, retrieves the average reading speed of that page. If desired,
        this reading speed can be adjusted to factor in difficulty. In all cases, the returned value is the average
        reading speed from all pages within the module.

        Note: Averages across pages, then students.

        :param module_num: The module number
        :param data448_id: A student's Data 448 id
        :return: a float representing reading speed in word per minute (WPM), the standard deviation for this average
        """
        page_reading_speeds = []
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        for page_num in module_paragraphs_dict[str(module_num)].keys():
            page_reading_speed, _ = self.page_reading_speed(module_num, int(page_num), data448_id)
            page_reading_speeds.append(page_reading_speed)

        return mean_and_sd(page_reading_speeds)

    def get_paragraph_list(self, module_num: int, page_num: int) -> [str]:
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        page_paragraphs = []
        for section_id, data in module_paragraphs_dict[str(module_num)][str(page_num)]['sections'].items():
            page_paragraphs += data['paragraphs']
        return page_paragraphs

    def get_num_pages_in_module(self, module_num: int) -> int:
        module_paragraphs = self.get_module_paragraphs_dict()
        return len(module_paragraphs[str(module_num)])

    def page_reading_duration(self, module_num: int, page_num: int, data448_id: int = None) -> (float, float):
        """
        Returns the page reading duration in minutes. Average of all students unless given a data_448 id.
        Additionally returns the standard deviation for student reading times used for its calculation.
        Standard deviation is None is a data448_id is given.
        """
        reading_duration_dict = self.get_reading_duration_dict()

        # Retrieve the correct DataFrame for the requested page.
        reading_duration_df = reading_duration_dict[f'{module_num}-{page_num}']
        reading_duration_df[DURATION_KEY] = reading_duration_df[END_TIME_KEY] - reading_duration_df[START_TIME_KEY]

        if data448_id:
            duration_ms = reading_duration_df[DURATION_KEY][f'{data448_id}']
            return ms_to_minutes(duration_ms), None

        mean_duration = ms_to_minutes(reading_duration_df[DURATION_KEY].mean())
        mean_duration_std = ms_to_minutes(reading_duration_df[DURATION_KEY].std())

        return mean_duration, mean_duration_std

    def page_reading_duration_list(self, module_num: int, page_num: int) -> [float]:
        """Returns a list of student page reading duration in minutes"""
        reading_duration_dict = self.get_reading_duration_dict()

        # Retrieve the correct DataFrame for the requested page.
        reading_duration_df = reading_duration_dict[f'{module_num}-{page_num}']
        reading_duration_df[DURATION_KEY] = reading_duration_df[END_TIME_KEY] - reading_duration_df[START_TIME_KEY]
        all_durations = [ms_to_minutes(d) for d in reading_duration_df[DURATION_KEY]]

        return all_durations

    def module_reading_duration(self, module_num: int, data448_id: int = None, mean=True) -> (float, float):
        """
        Returns the module reading duration (average of all page reading durations) in minutes.
        Average of all students unless given a data_448 id.
        Additionally returns the standard deviation for page reading times used for its calculation.
        Note: Averages across pages (which in turn are averages from all students)
        """

        num_pages = self.get_num_pages_in_module(module_num)
        page_durations = []

        for page_num in range(1, num_pages + 1):
            duration, _ = self.page_reading_duration(module_num, page_num, data448_id)
            page_durations.append(duration)

        return mean_and_sd(page_durations, mean)


def ms_to_minutes(duration_ms: float):
    return duration_ms / 1000 / 60


def mean_and_sd(values: [], mean=True) -> (float, float):
    values_list = list(values)
    if len(values_list) > 1:
        sd = statistics.stdev(values_list)
    else:
        sd = 0
    if mean:
        mean = sum(values_list) / len(values_list)
        return mean, sd
    else:
        return sum(values_list), sd


def get_text_difficulty_index(module_num: int, page_num: int = None) -> float:
    # TODO: read the data stored about the difficulty of each module/page and return the correctly difficulty index
    # TODO: switch so 0 means easy and 1 means difficult
    return 1
