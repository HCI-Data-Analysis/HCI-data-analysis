import pandas as pd
from pyunpack import Archive
import os
import json


def unzip_reading_logs_in_module(module_path: str):
    for data448_id in os.listdir(module_path):
        data448id_path = os.path.join(module_path, data448_id)
        for filename in os.listdir(data448id_path):
            print(filename)
            if filename.endswith('.zip'):
                Archive(os.path.join(data448id_path, filename)).extractall(os.path.join(data448id_path, filename))


def parse_reading_logs(module_path, module_paragraphs_path, module_number):
    """

    :param module_path: A string containing the path to the reading logs module
    :param module_number: A string containing the module number
    :return:
    """

    number_of_pages = get_num_pages_in_module(module_paragraphs_path, module_number)

    module = {module_number + "-" + str(page): pd.DataFrame() for page in range(1, number_of_pages+1)}

    for data448_id in os.listdir(module_path):
        data448id_path = os.path.join(module_path, data448_id)

        for reading_log_folder in os.listdir(data448id_path):
            reading_log_folder_path = os.path.join(data448id_path, reading_log_folder)
            convert_reading_logs_to_json(reading_log_folder_path)

            if os.path.isdir(reading_log_folder_path):
                for reading_log in os.listdir(reading_log_folder_path):
                    if '(' in reading_log:  #check for duplicate files
                        continue
                    # reading log file name in the format of
                    # 'COSC341-0-1-Reading-Logs.json', when splitting by '-':
                    # at index 1 is module number and index 2 is page number
                    # page_num = reading_log.split('-')[2]
                    page_num = reading_log.split('-')[2]
                    reading_log_path = os.path.join(reading_log_folder_path, reading_log)

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
                            # student_entry = pd.DataFrame.from_dict(reading_log_dict)

                            # print(reading_log_dict.keys())
                            # module_df = pd.DataFrame(columns=reading_log_dict.keys())
                        module[module_number + "-" + page_num] = module[module_number + "-" + page_num].append(reading_log_dict, ignore_index=True)
    print(module)
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


# def get_section_names():


if __name__ == "__main__":
    module_path = "../../data/api/canvas/reading_logs/741711"
    module_paragraphs_path = "../../data/module_paragraphs/module_paragraphs.json"
    # get_num_pages_in_module(module_paragraphs_path, "0")
    parse_reading_logs(module_path, module_paragraphs_path, '0')
    # unzip_reading_logs_in_module(MODULE_PATH)
