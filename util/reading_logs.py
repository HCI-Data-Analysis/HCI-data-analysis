import json
from random import random

from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH


cached_module_paragraphs_data: dict = {}


def get_module_paragraphs_dict() -> dict:
    try:
        f = open(MODULE_PARAGRAPHS_OUTPUT_FILEPATH, mode='r')
    except FileNotFoundError as e:
        raise FileNotFoundError(f'{e}\nRun "python parse_module_paragraphs.py" first.')
    module_paragraphs = json.load(f)

    return module_paragraphs


def get_average_adjusted_reading_speed(module_num: int, page_num: int, module_paragraphs_dict: dict = None) -> float:
    # in adjusted WPM/difficulty
    paragraph_list = get_paragraph_list(module_num, page_num, module_paragraphs_dict)
    difficulty = get_text_difficulty_index(' '.join(paragraph_list))

    num_words = len(' '.join(paragraph_list).split(' '))
    duration = get_average_page_reading_duration(module_num, page_num)

    # TODO: return WPM adjusted by difficulty
    return num_words / duration


def get_paragraph_list(module_num: int, page_num: int, module_paragraphs_dict: dict = None) -> [str]:
    if module_paragraphs_dict:
        module_paragraphs = module_paragraphs_dict
    else:
        module_paragraphs = get_module_paragraphs_dict()

    return module_paragraphs[str(module_num)][str(page_num)]['paragraphs']


def get_page_num_paragraphs(paragraphs_list: [str]) -> int:
    return len(paragraphs_list)


def get_average_page_reading_duration(module_num: int, page_num: int) -> float:
    """in minutes, average of all students"""
    # TODO: get average student reading duration for this page
    return random()


def get_text_difficulty_index(text: str) -> float:
    # TODO: fit regression?
    pass
