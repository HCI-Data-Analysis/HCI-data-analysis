import os.path

from scripts import graph_average_module_paragraph_reading_speed

MODULE_DIFFICULTY_LENGTH_FILEPATH = os.path.join('data', 'processed', 'paragraph_difficulty_length', 'pages')

if __name__ == '__main__':
    graph_average_module_paragraph_reading_speed(MODULE_DIFFICULTY_LENGTH_FILEPATH)
