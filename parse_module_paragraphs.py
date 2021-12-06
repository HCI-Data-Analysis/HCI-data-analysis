import os

from scripts.parse_module_paragraphs import parse_module_paragraphs
from util import MODULE_PARAGRAPHS_OUTPUT_FILEPATH

MODULE_LECTURES_PATH = os.path.join('data', 'modules', 'lectures')

if __name__ == '__main__':
    parse_module_paragraphs(MODULE_LECTURES_PATH, MODULE_PARAGRAPHS_OUTPUT_FILEPATH)
