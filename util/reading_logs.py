import json
from random import random

from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH


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
            difficulty = get_text_difficulty_index(' '.join(paragraph_list))
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


def page_reading_duration(module_num: int, page_num: int, data448_id: int = None) -> float:
    """Returns the page reading duration in minutes. Average of all students unless given a data_448 id."""
    # TODO: get average student reading duration for this page
    return random()


def module_reading_duration(module_num: int, data448_id: int = None) -> float:
    """Returns the module reading duration (average of all page reading durations) in minutes.
    Average of all students unless given a data_448 id. """
    # TODO: get average student reading duration for this page
    return random()


def get_text_difficulty_index(text: str) -> float:
    # TODO: fit regression?
    return 1
