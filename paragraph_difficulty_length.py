import os.path

from scripts.paragraph_difficulty_length import parse_module_paragraphs_with_difficulty_length

MODULE_PARAGRAPHS_FILEPATH = os.path.join('data', 'modules', 'module_paragraphs.json')
MODULES_PARAGRAPHS_PARSED_PATH = os.path.join('data', 'parsed', 'modules')
PAGES_PARAGRAPHS_PARSED_PATH = os.path.join('data', 'parsed', 'pages')
SECTIONS_PARAGRAPHS_PARSED_PATH = os.path.join('data', 'parsed', 'sections')


if __name__ == '__main__':
    parse_module_paragraphs_with_difficulty_length(MODULE_PARAGRAPHS_FILEPATH, MODULES_PARAGRAPHS_PARSED_PATH, PAGES_PARAGRAPHS_PARSED_PATH, SECTIONS_PARAGRAPHS_PARSED_PATH)
