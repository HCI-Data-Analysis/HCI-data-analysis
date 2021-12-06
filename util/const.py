import os.path

# all file paths stored in this file are defined assuming the starting point is the root directory
KEY_DIR = 'keys'
KEY_FILENAME = 'Key.csv'
KEY_PATH = os.path.join(KEY_DIR, KEY_FILENAME)

MODULE_PARAGRAPHS_OUTPUT_FILEPATH = os.path.join('data', 'processed', 'module_paragraphs.json')
