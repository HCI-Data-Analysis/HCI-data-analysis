import pandas as pd
import os
import json
import math
from schemas import CourseSchema


def parse_reading_logs_all(reading_log_path, module_paragraph_json_path) -> (dict, dict):
    """
    parse all reading logs, returns two dictionaries, each_continue_dict contains all the reading time stamp data,
    each_quiz_submit_dict contains all the quiz submit time stamp and answers
    :param reading_log_path: a string containing reading_log_path
    :param module_paragraph_json_path: a string containing where the parsed module_paragraph.json is stored
    :return: a tuple of dictionaries of dataframes.
                keys: in the format of [module_number]_[page_number]
                value: corresponding dataframe for either reading timestamp or quiz submission timestamp/answer
    """
    each_continue_dict = {}
    each_quiz_submit_dict = {}
    for module in os.listdir(reading_log_path):
        module_path = os.path.join(reading_log_path, module)
        module_num = CourseSchema.MODULE_NUM_KEY[int(module)]
        module_tuple = parse_reading_logs_module(module_path, module_paragraph_json_path, str(module_num))
        module_each_continue_dict = module_tuple[0]
        module_each_quiz_submit_dict = module_tuple[1]
        for k, v in module_each_continue_dict.items():
            each_continue_dict.setdefault(k, []).append(v)

        for k, v in module_each_quiz_submit_dict.items():
            each_quiz_submit_dict.setdefault(k, []).append(v)

    return each_continue_dict, each_quiz_submit_dict


def parse_reading_logs_module(module_path, module_paragraphs_path, module_number) -> (dict, dict):
    """
    Converts the reading log of given module_each_continue to two dictionary of dataframes. Both dictionary
     have the key in the format of [module_num]-[page_num]. The values being a dataframe that represents the reading log timestamp
    information for each students. The dataframe have columns of "start_time" [each section name] and
    "end_time", and rows with indexs of data448_id representing each student.
    :param module_path: A string containing the path to the reading logs module_each_continue
    :param module_paragraphs_path: A string containing the path of the module_paragraphs
    :param module_number: A string containing the module_each_continue number
    :return: a tuple with two dictionaries:
            module_each_continue:
                key format: [module_num]_[page_num]
                value: dataframes that have columns of "start_time" [each section name] and "end_time",
                        and have rows with indexs of data448_id representing each student.
            module_each_submit:
                key_format: [module_num]_[page_num]
                value: dataframes that have columns of "start_time" "submission_time" [question_number] and "end_time"
                        "submission_time" column contains a list of time stamps of when each submissions are made
                        the [question_number] columns contains a list of the answer the student chose for the
                        respective attempt.
                       dataframe have rows with index of data448_id representing each student.
    """

    number_of_pages = get_num_pages_in_module(module_paragraphs_path, module_number)

    module_each_continue = {f'{module_number}-{str(page)}': pd.DataFrame() for page in range(1, number_of_pages + 1)}
    module_each_submit = {f'{module_number}-{str(page)}': pd.DataFrame() for page in range(1, number_of_pages + 1)}

    for data448_id in os.listdir(module_path):
        # data448_id is a folder containing the student's reading logs. The folder's name is data448_id
        data448id_path = os.path.join(module_path, data448_id)

        # if reading logs in data448_id_path, then parse data448id_path, else
        contains_reading_log = False
        for reading_log_folder in os.listdir(data448id_path):
            reading_log_folder_path = os.path.join(data448id_path, reading_log_folder)
            convert_reading_logs_to_json(reading_log_folder_path)
            if reading_log_folder.endswith(".json"):
                contains_reading_log = True
                break

        if contains_reading_log:
            # TODO: if not correct reading log format, do not parse
            parsing_each_continue(data448id_path, module_number, data448_id, module_each_continue)
            parsing_each_quiz_submit(data448id_path, module_number, data448_id, module_each_submit)
        else:
            for reading_log_folder in os.listdir(data448id_path):
                reading_log_folder_path = os.path.join(data448id_path, reading_log_folder)
                if os.path.isdir(reading_log_folder_path) and reading_log_folder != "__MACOSX":
                    convert_reading_logs_to_json(reading_log_folder_path)
                    # TODO: if not correct reading log format, do not parse
                    parsing_each_continue(reading_log_folder_path, module_number, data448_id, module_each_continue)
                    parsing_each_quiz_submit(reading_log_folder_path, module_number, data448_id, module_each_submit)

    cleaned_module_each_continue = anomalies_deletion(module_each_continue)
    cleaned_module_each_submit = anomalies_deletion(module_each_submit)

    return cleaned_module_each_continue, cleaned_module_each_submit


def parsing_each_continue(reading_log_folder_path: str, module_number: str, data448_id: str, module: dict):
    for reading_log in os.listdir(reading_log_folder_path):
        reading_log_path = os.path.join(reading_log_folder_path, reading_log)

        if not reading_log.endswith('.json'):
            continue

        reading_log_name_array = reading_log.split('-')
        if '(' in reading_log and ')' in reading_log:  # check for duplicate files
            continue
        if reading_log_name_array[0] != "COSC341":  # make sure the file is a reading_log
            continue
        if reading_log_name_array[1] != module_number:  # make sure the reading log file is for the correct module
            continue

        # reading log file name in the format of
        # 'COSC341-0-1-Reading-Logs.json', when splitting by '-':
        # at index 1 is module number and index 2 is page number
        page_num = reading_log.split('-')[2]

        with open(reading_log_path, 'r') as f:
            try:
                reading_log_json = json.loads(f.read())
            except:
                continue

            # For each page, build a dictionary with:
            # keys of start_time, [section_names], end_time.
            # Values of corresponding time stamps
            reading_log_dict = {"start_time": reading_log_json['startTime'],
                                "end_time": reading_log_json['endTime']}

            for i in reading_log_json['eachContinue']:
                section_name = i['section']
                section_time = i['time']
                reading_log_dict[section_name] = section_time

        # converting dictionary to series so the row can be named with data448_id
        reading_log_series = pd.Series(reading_log_dict, name=data448_id)
        module[f'{module_number}-{page_num}'] = module[f'{module_number}-{page_num}'].append(reading_log_series)


def parsing_each_quiz_submit(reading_log_folder_path: str, module_number: str, data448_id: str, module: dict) -> (dict):
    for reading_log in os.listdir(reading_log_folder_path):
        reading_log_path = os.path.join(reading_log_folder_path, reading_log)

        if not reading_log.endswith('.json'):
            continue
        if '(' in reading_log and ')' in reading_log:  # check for duplicate files
            continue

        reading_log_name_array = reading_log.split('-')
        # print(reading_log_name_array)
        if reading_log_name_array[0] != "COSC341":  # make sure the file is a reading_log
            continue
        if reading_log_name_array[1] != module_number:  # make sure the reading log file is for the correct module
            continue

        # reading log file name in the format of
        # 'COSC341-0-1-Reading-Logs.json', when splitting by '-':
        # at index 1 is module number and index 2 is page number
        page_num = reading_log_name_array[2]

        with open(reading_log_path, 'r') as f:
            try:
                reading_log_json = json.loads(f.read())
            except:
                continue

            # For each page, build a dictionary with:
            # keys of start_time, quiz_submit_time, [question name], end_time.
            # Values of corresponding time stamps
            reading_log_dict = {"start_time": reading_log_json['startTime'],
                                "end_time": reading_log_json['endTime']}

            for i in reading_log_json['eachQuizSubmit']:
                for key, value in i.items():
                    if key in reading_log_dict:
                        # Key exist in dict.
                        # Check if type of value of key is list or not
                        if not isinstance(reading_log_dict[key], list):
                            # If type is not list then make it list
                            reading_log_dict[key] = [reading_log_dict[key]]
                        # Append the value in list
                        reading_log_dict[key].append(value)
                    else:
                        # As key is not in dict,
                        # so, add key-value pair
                        reading_log_dict[key] = value
        # converting dictionary to series so the row can be named with data448_id
        reading_log_series = pd.Series(reading_log_dict, name=data448_id)
        module[f'{module_number}-{page_num}'] = module[f'{module_number}-{page_num}'].append(reading_log_series)


def anomalies_deletion(module: dict) -> dict:
    for key, value in module.items():
        # if more than half of the data in a column is NA, drop the column
        value.dropna(axis='columns', thresh=math.floor(len(value) / 2), inplace=True)
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
