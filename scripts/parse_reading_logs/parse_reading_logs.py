import pandas as pd
from pyunpack import Archive
import os
import json
import math


def unzip_reading_logs_in_module(module_path: str):
    for data448_id in os.listdir(module_path):
        data448id_path = os.path.join(module_path, data448_id)
        for filename in os.listdir(data448id_path):
            print(filename)
            if filename.endswith('.zip'):
                Archive(os.path.join(data448id_path, filename)).extractall(os.path.join(data448id_path, filename))


def parse_reading_logs(module_path, module_paragraphs_path, module_number):
    """
    Converts the reading log of given module to a dictionary of dataframes, with the key being
    [module_num]-[page_num] and the values being a dataframe that represents the reading log timestamp
    information for each students. The dataframe have columns of "start_time" [each section name] and
    "end_time", and rows with indexs of data448_id representing each student.
    :param module_path: A string containing the path to the reading logs module
    :param module_paragraphs_path: A string containing the path of the module_paragraphs
    :param module_number: A string containing the module number
    :return:
    """

    number_of_pages = get_num_pages_in_module(module_paragraphs_path, module_number)

    module = {module_number + "-" + str(page): pd.DataFrame() for page in range(1, number_of_pages+1)}

    for data448_id in os.listdir(module_path):
        data448id_path = os.path.join(module_path, data448_id)

        # if reading logs in data448_id_path, then parse data448id_path, else
        contains_reading_log = False
        for reading_log_folder in os.listdir(data448id_path):
            if reading_log_folder.endswith(".json"):
                contains_reading_log = True

        if contains_reading_log:
            parsing_reading_log_json(data448id_path, module_number, data448_id, module)
        else:
            for reading_log_folder in os.listdir(data448id_path):
                reading_log_folder_path = os.path.join(data448id_path, reading_log_folder)
                if os.path.isdir(reading_log_folder_path):
                    if reading_log_folder != "__MACOSX":
                        parsing_reading_log_json(reading_log_folder_path, module_number, data448_id, module)

    cleaned_module = anomolies_deletion(module)
    return cleaned_module


def parsing_reading_log_json(reading_log_folder_path: str, module_number: str, data448_id: str, module: dict):
    convert_reading_logs_to_json(reading_log_folder_path)
    for reading_log in os.listdir(reading_log_folder_path):
        reading_log_path = os.path.join(reading_log_folder_path, reading_log)
        # print(reading_log_path)
        # if os.path.isdir(reading_log_path):
        # print("AAAAAAAAAA")
        if not reading_log.endswith('.json'):
            continue
        if '(' in reading_log:  # check for duplicate files
            continue
        if reading_log.split('-')[0] != "COSC341":
            continue

        page_num = reading_log.split('-')[2]
        # reading log file name in the format of
        # 'COSC341-0-1-Reading-Logs.json', when splitting by '-':
        # at index 1 is module number and index 2 is page number
        # page_num = reading_log.split('-')[2]
        # print(reading_log_path)
        with open(reading_log_path, 'r') as f:
            reading_log_json = json.loads(f.read())
            # For each page, build a dictionary with:
            # keys of start_time, [section_names], end_time.
            # Values of corresponding time stamps
            reading_log_dict = {"start_time": reading_log_json['startTime']}

            for i in reading_log_json['eachContinue']:
                section_name = i['section']
                section_time = i['time']
                reading_log_dict[section_name] = section_time

            reading_log_dict['end_time'] = reading_log_json['endTime']

        mod_num_page_num = module_number + "-" + page_num
        reading_log_series = pd.Series(reading_log_dict, name=data448_id)
        module[mod_num_page_num] = module[mod_num_page_num].append(reading_log_series)


def anomolies_deletion(module: dict) -> (dict):

    for key, value in module.items():
        # if more than half of the data in a column is NA, drop the column
        value.dropna(axis='columns', thresh=math.floor(len(value)/2), inplace=True)
        value.dropna(axis='index', how="any", inplace=True)

    return module


def get_num_pages_in_module(module_paragraphs_path, module_number):
    try:
        with open(module_paragraphs_path, 'r') as f:
            module_paragraphs = f.read()
            try:
                json_file = json.loads(module_paragraphs)
                return len(json_file[module_number])
            except ValueError as e:
                print("invalid json file")
    except FileNotFoundError:
        print("module_paragraph.json not found!!")


def convert_reading_logs_to_json(reading_log_path):
    if os.path.isdir(reading_log_path):
        for file in os.listdir(reading_log_path):
            if file.endswith(".txt"):
                file_path = os.path.join(reading_log_path, file)
                os.rename(src=file_path, dst=file_path.replace('.txt', '.json'))
