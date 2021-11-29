import os.path

from scripts.paragraph_difficulty_length import analyze_difficulty_length_module_paragraphs

MODULE_PARAGRAPHS_FILEPATH = os.path.join('data', 'modules', 'module_paragraphs.json')


if __name__ == '__main__':
    analyze_difficulty_length_module_paragraphs(MODULE_PARAGRAPHS_FILEPATH)
