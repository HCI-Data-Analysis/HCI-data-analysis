import json
import os.path

import pandas as pd

from util.readability import get_flesch_reading_ease


def parse_module_paragraphs_with_difficulty_length(module_paragraphs_filepath, parsed_modules_paragraphs_path,
                                                   parsed_pages_paragraphs_path, parsed_sections_paragraphs_path):
    """
    Perform a difficulty and length analysis on the module paragraphs
    :param module_paragraphs_filepath: Filepath of the module paragraphs data
    :param parsed_sections_paragraphs_path: Path of the parsed sections data
    :param parsed_modules_paragraphs_path: Path of the parsed modules data
    :param parsed_pages_paragraphs_path: Path of the pages module data
    """

    with open(module_paragraphs_filepath, 'r') as f:
        m_p_raw = f.read()
        module_paragraphs_raw_data = json.loads(m_p_raw)

    modules_data_frame = pd.DataFrame(
        columns=['module', 'total_paragraphs', 'average_paragraph_length_words',
                 'average_paragraph_length_chars', 'average_flesch_reading_ease']
    )

    for module in module_paragraphs_raw_data:
        pages_data_frame = pd.DataFrame(
            columns=['page', 'title', 'total_paragraphs', 'average_paragraph_length_words',
                     'average_paragraph_length_chars', 'average_flesch_reading_ease']
        )

        module_module_data = {
            'module': module,
            'total_paragraphs': 0,
            'average_paragraph_length_words': 0,
            'average_paragraph_length_chars': 0,
            'average_flesch_reading_ease': 0
        }

        for page in module_paragraphs_raw_data[module]:
            sections_data_frame = pd.DataFrame(
                columns=['section', 'title', 'total_paragraphs', 'average_paragraph_length_words',
                         'average_paragraph_length_chars', 'average_flesch_reading_ease']
            )

            page_data = module_paragraphs_raw_data[module][page]
            page_module_data = {
                'page': page,
                'title': page_data['title'],
                'total_paragraphs': 0,
                'average_paragraph_length_words': 0,
                'average_paragraph_length_chars': 0,
                'average_flesch_reading_ease': 0
            }

            for section in page_data['sections']:
                section_data = module_paragraphs_raw_data[module][page]['sections'][section]

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

                page_module_data['total_paragraphs'] += total_paragraphs
                page_module_data['average_paragraph_length_words'] += average_paragraph_length_words / len(
                    page_data['sections'])
                page_module_data['average_paragraph_length_chars'] += average_paragraph_length_chars / len(
                    page_data['sections'])
                page_module_data['average_flesch_reading_ease'] += average_flesch_reading_ease / len(
                    page_data['sections'])

                module_module_data['total_paragraphs'] += total_paragraphs
                module_module_data['average_paragraph_length_words'] += average_paragraph_length_words / len(
                    page_data['sections']) / len(module_paragraphs_raw_data[module])
                module_module_data['average_paragraph_length_chars'] += average_paragraph_length_chars / len(
                    page_data['sections']) / len(module_paragraphs_raw_data[module])
                module_module_data['average_flesch_reading_ease'] += average_flesch_reading_ease / len(
                    page_data['sections']) / len(module_paragraphs_raw_data[module])

                section_page_data = {
                    'section': section,
                    'title': section_data['title'],
                    'total_paragraphs': total_paragraphs,
                    'average_paragraph_length_words': average_paragraph_length_words,
                    'average_paragraph_length_chars': average_paragraph_length_chars,
                    'average_flesch_reading_ease': average_flesch_reading_ease
                }
                sections_data_frame = sections_data_frame.append(section_page_data, ignore_index=True)
            sections_data_frame.to_csv(
                os.path.join(
                    parsed_sections_paragraphs_path,
                    f'sections_page_{page}_module_{module}_difficulty_length.csv'
                ),
                index=False
            )
            pages_data_frame = pages_data_frame.append(page_module_data, ignore_index=True)
        pages_data_frame.to_csv(
            os.path.join(parsed_pages_paragraphs_path, f'pages_module_{module}_difficulty_length.csv'),
            index=False
        )
        print('FINAL MODULE', module, ':', module_module_data)
        modules_data_frame = modules_data_frame.append(module_module_data, ignore_index=True)
    modules_data_frame.to_csv(
        os.path.join(parsed_modules_paragraphs_path, f'modules_difficulty_length.csv'),
        index=False
    )
