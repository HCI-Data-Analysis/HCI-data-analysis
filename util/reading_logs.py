import json
import pandas as pd
from random import random

from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH
from scripts import parse_reading_logs_module


class ReadingLogsData:
    module_paragraphs_dict = None

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
        duration = page_reading_duration(module_num, page_num, data448_id)

        if adjust_for_difficulty:
            difficulty = get_text_difficulty_index(module_num, page_num)
            # TODO: return WPM adjusted by difficulty

        return num_words / duration

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
        module_paragraphs_dict = self.module_paragraphs_dict()
        for page_num in module_paragraphs_dict[str(module_num)].keys():
            return self.page_reading_speed(module_num, int(page_num), data448_id, adjust_for_difficulty)

        return sum(page_reading_speeds) / len(page_reading_speeds)

    def get_paragraph_list(self, module_num: int, page_num: int) -> [str]:
        module_paragraphs = self.get_module_paragraphs_dict()
        return module_paragraphs[str(module_num)][str(page_num)]['paragraphs']

    def content_quiz_performance(self, module_path, module_number) ->(dict):
        cleaned_module_each_continue, cleaned_module_each_submit = parse_reading_logs_module(module_path, MODULE_PARAGRAPHS_OUTPUT_FILEPATH, module_number)
        content_quiz_performance = {}
        for reading_log_headers, pages in cleaned_module_each_submit.items():
            print(pages)
            data448_id = pages.index.values
            page_quiz_performance = {}
            for row in pages.iterrows():
                num_attempt_to_correct = 0
                num_first_attmept_correct = False
                for index, element in row.items():
                    if type(element) is list:
                        if isinstance(element[0], str) &element[0] == "ans":
                            num_first_attmept_correct = True
                        elif isinstance(element[0], str):
                            for submit in element:
                                if submit != "ans":
                                    num_attempt_to_correct += 1
                                else:
                                    break
                    page_quiz_performance[index] = [num_first_attmept_correct, num_attempt_to_correct]
            page_quiz_series = pd.Series(page_quiz_performance, name=data448_id)
            content_quiz_performance[reading_log_headers] = content_quiz_performance[reading_log_headers].append(page_quiz_series)
            
        return content_quiz_performance




def page_reading_duration(module_num: int, page_num: int, data448_id: int = None) -> float:
    """Returns the page reading duration in minutes. Average of all students unless given a data_448 id."""
    # TODO: get average student reading duration for this page
    return random()


def module_reading_duration(module_num: int, data448_id: int = None) -> float:
    """Returns the module reading duration (average of all page reading durations) in minutes.
    Average of all students unless given a data_448 id. """
    # TODO: get average student reading duration for this page
    return random()


def get_text_difficulty_index(module_num: int, page_num: int = None) -> float:
    # TODO: read the data stored about the difficulty of each module/page and return the correctly difficulty index
    return 1


if __name__ == "__main__":
    READING_LOG_PATH = "data/api/canvas/reading_logs"
    x = ReadingLogsData()
    x.content_quiz_performance(READING_LOG_PATH, MODULE_PARAGRAPHS_OUTPUT_FILEPATH)