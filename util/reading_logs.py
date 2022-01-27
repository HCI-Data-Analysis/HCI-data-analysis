import json
import os
import statistics
import pandas as pd
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
        average reading speed of that page.

        Returns None if this page has no content quiz questions.
        Standard deviation is None if a data448_id is given.

        :param module_num: The module number
        :param page_num: The page number
        :param data448_id: A student's Data 448 id
        :return: (float representing the average number of content quiz attempts, standard deviation for this average)
        """
        page_content_quiz_df = self.get_content_quiz_performance_dict()[f'{module_num}-{page_num}']
        TAMPERED = -1

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
                    return count
                else:
                    count += 1

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
            average_num_attempts, _ = self.page_content_quiz_num_attempts(module_num, int(page_num), data448_id)
            content_quiz_attempts_per_page.append(average_num_attempts)

        return aggregate_and_sd(content_quiz_attempts_per_page)

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

        return aggregate_and_sd(page_durations, mean)

    def content_quiz_performance(self) -> dict:
        """

        :return: A dictionary with keys in the format of [module_num]_[page_num] and values of a list:
                    number of entries, a list of number of attempts each students used,
                    a list of grades each student get on their first attempt, number of total attempts
        """
        content_quiz_dict = self.get_content_quiz_performance_dict()
        num_attempt_to_correct = {}
        for reading_log_headers, page in content_quiz_dict.items():
            number_of_entries = 0
            num_attempt = []
            first_attempt_grade = []
            num_questions = len(page.columns)-3
            for student in page.iterrows():
                for series in student:
                    num_corrects = 0
                    if isinstance(series, pd.Series):
                        for index, elements in series.items():
                            if isinstance(elements, str):
                                number_of_entries += 1
                                num_attempt.append(1)
                                if elements == "ans":
                                    num_corrects += 1
                            elif isinstance(elements, list):
                                if isinstance(elements[0], str):
                                    number_of_entries += 1
                                    individual_attempts = 0
                                    for submit in elements:
                                        if submit != 'ans':
                                            individual_attempts += 1
                                        else:
                                            individual_attempts += 1
                                            num_attempt.append(individual_attempts)
                                            break
                                    if elements[0] == "ans":
                                        num_corrects += 1
                if num_questions > 0:
                    student_first_attempt_grade = num_corrects/num_questions
                    first_attempt_grade.append(student_first_attempt_grade)
            performance_list = [number_of_entries, num_attempt, first_attempt_grade, sum(num_attempt)]
            num_attempt_to_correct[reading_log_headers] = performance_list



        # content_quiz_performance_dict = {}
        # for reading_log_headers, pages in cleaned_module_each_submit.items():
        #     print(pages)
        #     data448_id = pages.index.values
        #     page_quiz_performance = {}
        #     for row in pages.iterrows():
        #         num_attempt_to_correct = 0
        #         num_first_attempt_correct = False
        #         for index, element in row.items():
        #             if type(element) is list:
        #                 if isinstance(element[0], str) & element[0] == "ans":
        #                     num_first_attempt_correct = True
        #                 elif isinstance(element[0], str):
        #                     for submit in element:
        #                         if submit != "ans":
        #                             num_attempt_to_correct += 1
        #                         else:
        #                             break
        #             page_quiz_performance[index] = [num_first_attempt_correct, num_attempt_to_correct]
        #     page_quiz_series = pd.Series(page_quiz_performance, name=data448_id)
        #     content_quiz_performance_dict[reading_log_headers] = content_quiz_performance_dict[
        #         reading_log_headers].append(
        #         page_quiz_series)

        return num_attempt_to_correct


def ms_to_minutes(duration_ms: float):
    return duration_ms / 1000 / 60


def aggregate_and_sd(values: [], mean=True) -> (float, float):
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

