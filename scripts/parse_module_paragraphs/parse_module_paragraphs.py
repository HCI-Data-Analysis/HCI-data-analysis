import json
import os
import re

from bs4 import BeautifulSoup


def parse_module_paragraphs(module_lectures_path, output_filepath):
    """
    Reads a folder containing lecture html data, reads the paragraphs within each content section
    and writes it to a dict, then as a json to the output filepath
    :param module_lectures_path: Path where the lecture html data is
    :param output_filepath: Filepath where the new file will be written
    """

    module_paragraphs = {}

    for i in os.listdir(module_lectures_path):
        if i.endswith('.html'):
            full_path = os.path.join(module_lectures_path, i)
            module_data = re.findall(r'\d+', i)
            if len(module_data) >= 2:
                module = module_data[0]
                module_page = module_data[1]
                module_paragraphs.setdefault(module, {})
                module_paragraphs[module].setdefault(module_page, {
                    'name': i[(len(module) + len(module_page) + 1):].replace('.html', ''),
                    'sections': {}
                })
                with open(full_path, 'r', encoding='utf-8') as f:
                    full_html = f.read()
                    soup = BeautifulSoup(full_html, 'html.parser')
                    header_data = soup.find('div', class_='header')
                    header_parsed = parse_html_contents(header_data)
                    module_paragraphs[module][module_page]['title'] = header_parsed
                    divs_content_section = soup.find_all('div', class_='content-section')
                    for index, div in enumerate(divs_content_section, start=1):
                        title = div.find('h2')
                        module_paragraphs[module][module_page]['sections'][index] = {
                            'title': parse_html_contents(title),
                            'paragraphs': []
                        }
                        paragraphs = div.find_all('p')
                        for paragraph in paragraphs:
                            paragraph_parsed = parse_html_contents(paragraph)
                            if paragraph_parsed != '':
                                module_paragraphs[module][module_page]['sections'][index]['paragraphs'].append(
                                    paragraph_parsed)
                        quotes = div.find_all('blockquote')
                        if quotes:
                            quote_paragraph = ''
                            for quote in quotes:
                                quote_parsed = parse_html_contents(quote)
                                quote_paragraph += quote_parsed
                            module_paragraphs[module][module_page]['sections'][index]['paragraphs'].append(
                                quote_paragraph)

    with open(output_filepath, 'w') as f:
        f.write(json.dumps(module_paragraphs, indent=4))


def parse_html_contents(tag_element):
    """
    Remove extraneous characters from an html string
    :param tag_element: Tag element to get inner contents from
    :return: Parsed string
    """
    html_content = ''
    for content in tag_element.contents:
        html_content += str(content.string)
    parsed = html_content.replace('\n', '').replace('\t', '').strip()
    parsed = re.sub(' +', ' ', parsed)
    return parsed
