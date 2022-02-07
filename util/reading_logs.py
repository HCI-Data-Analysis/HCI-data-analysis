import json
import os
import numpy as np
import pandas as pd
from random import random

import dill
import pandas as pd

from schemas import CourseSchema
from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH, CACHE_FOLDER

START_TIME_KEY = 'start_time'
END_TIME_KEY = 'end_time'
DURATION_KEY = 'duration'
TAMPERED = -1


class ReadingLogsData:
    module_paragraphs_dict = None
    reading_duration_dict = None
    content_quiz_performance_dict = None

    def exclude_outliers(self):
        """
        Utility method to remove outliers from the class instance versions of the reading/content quiz dictionaries.
        Modifies these dictionaries so each DataFrame within them removes the ignored ids. This method is called within
        self.get_parsed_reading_log_data() so all further analysis factors it in inherently.
        """
        excluded_ids = [f'{i}' for i in CourseSchema.OUTLIER_DATA448_IDS]  # DF indexes are strings
        dicts_of_dfs = [self.reading_duration_dict, self.content_quiz_performance_dict]
        for dict_df in dicts_of_dfs:
            for _, df in dict_df.items():
                try:
                    df.drop(excluded_ids, inplace=True)
                except KeyError:
                    continue

    def get_module_paragraphs_dict(self) -> dict:
        if self.module_paragraphs_dict:
            return self.module_paragraphs_dict

        try:
            f = open(MODULE_PARAGRAPHS_OUTPUT_FILEPATH, mode='r')
        except FileNotFoundError as e:
            raise FileNotFoundError(f'{e}\nRun "python parse_module_paragraphs.py" first.')

        module_paragraphs = json.load(f)
        self.module_paragraphs_dict = module_paragraphs
        return self.module_paragraphs_dict

    def get_parsed_reading_log_data(self) -> (dict, dict):
        if not self.reading_duration_dict or not self.content_quiz_performance_dict:
            try:
                with open(os.path.join(CACHE_FOLDER, 'reading_durations_dict.pkl'), 'rb') as f:
                    self.reading_duration_dict = dill.load(f)
                with open(os.path.join(CACHE_FOLDER, 'content_quiz_performance_dict.pkl'), 'rb') as f:
                    self.content_quiz_performance_dict = dill.load(f)
            except FileNotFoundError as e:
                raise FileNotFoundError(f'{e}\nRun "python parse_reading_logs.py" first.')
            self.exclude_outliers()

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
        for the page. Without a data448_id, retrieves the average reading speed of that page.

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

        return aggregate_and_sd(student_reading_speeds)

    def module_reading_speed(self, module_num: int, data448_id: int = None) -> (float, float):
        """
        Retrieves the reading speed for a module. If given a data448_id, only retrieves that student's reading speed
        for the page. Without a data448_id, retrieves the average reading speed of that page. In all cases,
        the returned value is the average reading speed from all pages within the module.

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

        return aggregate_and_sd(page_reading_speeds)

    def page_content_quiz_num_attempts(self, module_num: int, page_num: int, data448_id: int = None) -> (float, float):
        """
        Retrieves the average number of content quiz attempts before a correct answer for a page. If given a
        data448_id, only retrieves that student's reading speed for the page. Without a data448_id, retrieves the
        average number of attempts of that page.

        Returns None if this page has no content quiz questions.
        Standard deviation is None if a data448_id is given.

        :param module_num: The module number
        :param page_num: The page number
        :param data448_id: A student's Data 448 id
        :return: (float representing the average number of content quiz attempts, standard deviation for this average)
        """
        page_content_quiz_df = self.get_content_quiz_performance_dict()[f'{module_num}-{page_num}']

        zip_set = [page_content_quiz_df[col] for col in page_content_quiz_df if col.startswith('q')]
        if not zip_set:
            return None

        page_content_quiz_df['num_before_ans'] = [num_before_ans(*a) for a in zip(*zip_set)]

        if data448_id:
            return page_content_quiz_df['num_before_ans'][f'{data448_id}'], None

        all_num_attempts = [num for num in page_content_quiz_df['num_before_ans'].values if num != TAMPERED]
        return aggregate_and_sd(all_num_attempts)

    def module_content_quiz_num_attempts(self, module_num: int, data448_id: int = None) -> (float, float):
        content_quiz_attempts_per_page = []
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        for page_num in module_paragraphs_dict[str(module_num)].keys():
            page_attempts = self.page_content_quiz_num_attempts(module_num, int(page_num), data448_id)
            if page_attempts is not None:
                average_num_attempts = page_attempts[0]
                content_quiz_attempts_per_page.append(average_num_attempts)

        return aggregate_and_sd(content_quiz_attempts_per_page)

    def page_content_quiz_attempts_list(self, module_num: int, page_num: int) -> [float]:
        """
        returns a list of extra attempts each student took for the content quiz of the given page
        :param module_num: The module number
        :param page_num: The page number
        :return:
        """
        page_content_quiz_df = self.get_content_quiz_performance_dict()[f'{module_num}-{page_num}']

        zip_set = [page_content_quiz_df[col] for col in page_content_quiz_df if col.startswith('q')]
        if not zip_set:
            return None

        page_content_quiz_df['num_before_ans'] = [num_before_ans(*a) for a in zip(*zip_set)]

        all_num_attempts = [num for num in page_content_quiz_df['num_before_ans'].values if num != TAMPERED]

        return all_num_attempts

    def page_content_quiz_first_attempt_grade(self, module_num: int, page_num: int, data448_id: int = None) -> float:
        """
        Retrieves the average first attempt grade for content quiz. If given a data448_id, only retrieves that student's
        reading speed for the page. Without a data448_id, retrieves the average first attempt grade of that page.

        Returns None if this page has no content quiz questions.

        :param module_num: The module number
        :param page_num: The page number
        :param data448_id: A student's Data 448 id
        :return: (float representing the average first attempt grade of the given content quiz, standard deviation of
        this average)
        """

        page_content_quiz_df = self.get_content_quiz_performance_dict()[f'{module_num}-{page_num}']

        zip_set = [page_content_quiz_df[col] for col in page_content_quiz_df if col.startswith('q')]

        if not zip_set:
            return None

        cols = [col for col in page_content_quiz_df if col.startswith('q')]
        questions_df = page_content_quiz_df[cols]

        def first_attempt_grade(row):
            count = 0
            for element in row:
                if element == 'ans' or element[0] == 'ans':
                    count += 1
            return count/len(row)

        questions_df['first_attempt_grade'] = questions_df.apply(lambda x: first_attempt_grade(x), axis=1)

        if data448_id:
            return questions_df['first_attempt_grade'][f'{data448_id}'], None

        return aggregate_and_sd(questions_df['first_attempt_grade'])

    def module_content_quiz_first_attempt_grade(self, module_num: int, data448_id: int = None) -> (float, float):
        content_quiz_first_attempt_grade = []
        module_paragraphs_dict = self.get_module_paragraphs_dict()
        for page_num in module_paragraphs_dict[str(module_num)].keys():
            page_grade = self.page_content_quiz_first_attempt_grade(module_num, int(page_num), data448_id)
            if page_grade is not None:
                average_grade = page_grade[0]
                content_quiz_first_attempt_grade.append(average_grade)

        return aggregate_and_sd(content_quiz_first_attempt_grade)

    def content_quiz_first_attempt_grade_list(self, module_num: int, page_num: int):
        """
        Returns the list of student's firat attempt grade for the given page
        :param module_num: the module number
        :param page_num: the page number
        :return:
        """
        page_content_quiz_df = self.get_content_quiz_performance_dict()[f'{module_num}-{page_num}']

        zip_set = [page_content_quiz_df[col] for col in page_content_quiz_df if col.startswith('q')]

        if not zip_set:
            return None

        cols = [col for col in page_content_quiz_df if col.startswith('q')]
        questions_df = page_content_quiz_df[cols]

        def first_attempt_grade(row):
            count = 0
            for element in row:
                if element == 'ans' or element[0] == 'ans':
                    count += 1
            return count / len(row)

        questions_df['first_attempt_grade'] = questions_df.apply(lambda x: first_attempt_grade(x), axis=1)

        return [*questions_df['first_attempt_grade']]

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
        end_time_key = self.get_last_non_review_section_name(module_num, page_num)
        reading_duration_df[DURATION_KEY] = reading_duration_df[end_time_key] - reading_duration_df[START_TIME_KEY]

        if data448_id:
            duration_ms = reading_duration_df[DURATION_KEY][f'{data448_id}']
            return ms_to_minutes(duration_ms), None

        mean_duration = ms_to_minutes(reading_duration_df[DURATION_KEY].mean())
        mean_duration_std = ms_to_minutes(reading_duration_df[DURATION_KEY].std())

        return mean_duration, mean_duration_std

    def is_reading_log_file(reading_log_file_name) -> bool:
        if not reading_log_file_name.endswith('.json'):
            return False
        if '(' in reading_log_file_name and ')' in reading_log_file_name:  # check for duplicate files
            return False

        reading_log_name_array = reading_log_file_name.split('-')
        if reading_log_name_array[0] != "COSC341" & reading_log_name_array[3] != "Reading" & reading_log_name_array[
            4] != "Logs":  # make sure the file is a reading_log
            return False

    def page_reading_duration_list(self, module_num: int, page_num: int) -> [float]:
        """Returns a list of student page reading duration in minutes"""
        reading_duration_dict = self.get_reading_duration_dict()

        # Retrieve the correct DataFrame for the requested page.
        reading_duration_df = reading_duration_dict[f'{module_num}-{page_num}']
        end_time_key = self.get_last_non_review_section_name(module_num, page_num)
        reading_duration_df[DURATION_KEY] = reading_duration_df[end_time_key] - reading_duration_df[START_TIME_KEY]
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

        return aggregate_and_sd(page_durations, mean)

    def get_last_non_review_section_name(self, module_num: int, page_num: int) -> str:
        module_sections_dict = self.get_module_paragraphs_dict()[f'{module_num}'][f'{page_num}']['sections']

        last_section_title = list(module_sections_dict.values())[-1]
        if last_section_title == 'Review Form':
            last_section_title = list(module_sections_dict.values())[-2]

        return last_section_title['title']


def ms_to_minutes(duration_ms: float):
    return duration_ms / 1000 / 60


def aggregate_and_sd(values: [], mean=True) -> (float, float):
    values_list = list(values)
    if len(values_list) > 1:
        sd = np.std(values_list)
    else:
        sd = 0
    if mean:
        mean = sum(values_list) / len(values_list)
        return mean, sd
    else:
        return sum(values_list), sd


def num_before_ans(*args):
    q_response_lists = []
    for val in args:
        q_response_lists.append(val) if isinstance(val, list) else q_response_lists.append([val])

    # Discard if they tampered with the numbers so questions have a different number of attempts
    if not all(len(response_set) == len(q_response_lists[0]) for response_set in q_response_lists):
        return TAMPERED

    all_correct = ['ans'] * len(q_response_lists)
    count = 0
    for q_response_set in zip(*q_response_lists):
        if list(q_response_set) == all_correct:
            return count / len(q_response_lists)
        else:
            count += 1

