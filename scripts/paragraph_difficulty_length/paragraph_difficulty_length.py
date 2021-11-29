import json

import pandas as pd

from util.readability import get_flesch_reading_ease


def analyze_difficulty_length_module_paragraphs(module_paragraphs_filepath):
    """
    Perform a difficulty and length analysis on the module paragraphs
    :param module_paragraphs_filepath: Filepath of the module paragraphs data
    """

    with open(module_paragraphs_filepath, 'r') as f:
        m_p_raw = f.read()
        module_paragraphs_raw_data = json.loads(m_p_raw)

    modules_data = []
    for module in module_paragraphs_raw_data:
        data_frame = pd.DataFrame(
            columns=['section', 'total_paragraphs', 'average_paragraph_length_words', 'average_paragraph_length_char',
                     'average_flesch_reading_ease']
        )
        per_module_data = {
            'section': "0",
            'total_paragraphs': 0,
            'average_paragraph_length_words': 0,
            'average_paragraph_length_chars': 0,
            'average_flesch_reading_ease': 0
        }
        for section in module_paragraphs_raw_data[module]:
            section_data = module_paragraphs_raw_data[module][section]
            total_paragraphs = len(section_data['paragraphs'])
            average_paragraph_length_words = (sum(
                len(paragraph.split(' ')) for paragraph in section_data['paragraphs']
            ) / total_paragraphs) if total_paragraphs > 0 else 0
            average_paragraph_length_chars = (sum(
                len(paragraph) for paragraph in section_data['paragraphs']
            ) / total_paragraphs) if total_paragraphs > 0 else 0
            average_flesch_reading_ease = sum(
                get_flesch_reading_ease(paragraph) for paragraph in section_data['paragraphs']
            ) / total_paragraphs if total_paragraphs > 0 else 1

            per_module_data['total_paragraphs'] += total_paragraphs
            per_module_data['average_paragraph_length_words'] += average_paragraph_length_words
            per_module_data['average_paragraph_length_chars'] += average_paragraph_length_chars
            per_module_data['average_flesch_reading_ease'] += average_flesch_reading_ease
            data = {
                'section': section,
                'total_paragraphs': total_paragraphs,
                'average_paragraph_length_words': average_paragraph_length_words,
                'average_paragraph_length_chars': average_paragraph_length_chars,
                'average_flesch_reading_ease': average_flesch_reading_ease
            }
            data_frame = data_frame.append(data, ignore_index=True)
        per_module_data['total_paragraphs'] /= len(module_paragraphs_raw_data[module])
        per_module_data['average_paragraph_length_words'] /= len(module_paragraphs_raw_data[module])
        per_module_data['average_paragraph_length_chars'] /= len(module_paragraphs_raw_data[module])
        per_module_data['average_flesch_reading_ease'] /= len(module_paragraphs_raw_data[module])
        print('Module', module, ': ', per_module_data)
        data_frame = data_frame.append(per_module_data, ignore_index=True)
        modules_data.append(data_frame)

    print(modules_data)
