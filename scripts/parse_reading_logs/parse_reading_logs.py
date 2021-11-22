import pandas as pd
from pyunpack import Archive
import os
import json


def unzip_reading_logs_in_module(module_path:str):
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
    df_columns = []

    for page in range(1, number_of_pages):
        df_columns.append('module:' + module_number + '_page:' + str(page))
    df_module = pd.DataFrame(columns=df_columns)

    for data448_id in os.listdir(module_path):
        data448id_path = os.path.join(module_path, data448_id)
        for reading_log_folder in os.listdir(data448id_path):
            reading_log_folder_path = os.path.join(data448id_path, reading_log_folder)
            if os.path.isdir(reading_log_folder_path):
                for reading_log in os.listdir(reading_log_folder_path):
                    reading_log_path = os.path.join(reading_log_folder_path, reading_log)
                    with open(reading_log_path, 'r') as f:
                        reading_log_content = f.read()
                        reading_log_json = json.dumps(reading_log_content)
                        reading_log_dict = json.loads(reading_log_json)  # this is a god damn string for some reason
                        df_reading_log_columns = ["start_time"]
                        # print(reading_log_dict.get("eachContinue"))
                        # for i in reading_log_dict['eachContinue']:
                        #     print(i)
                        df_reading_log = pd.DataFrame(columns=reading_log_dict.keys())


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


if __name__ == "__main__":
    module_path = "../../data/api/canvas/reading_logs/741711"
    module_paragraphs_path = "../../data/module_paragraphs/module_paragraphs.json"
    # get_num_pages_in_module(module_paragraphs_path, "0")
    parse_reading_logs(module_path, module_paragraphs_path, '0')
    #unzip_reading_logs_in_module(MODULE_PATH)
