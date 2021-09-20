import os
import numpy as np
import pandas as pd
import re
import shutil


def convert_name(name):
    """Helper method that converts full name into zip file format"""
    names = name.split(' ')
    new_name = ''
    for item in reversed(names[0]):
        new_name += re.sub(r'[^a-zA-Z ]+', '', item).lower()
    return new_name


def zip_anonymize(zip_filepath, output_path, keys_filepath):
    """Outputs a collection of files to <output_filepath> that contains the anonymized versions of zip files specified in
    <zip_filepath>, using the keys file located in <keys_filepath>

    :param zip_filepath: A string containing the filepath of the zip files to be anonymized
    :param output_path: A string containing the path where the anonymized files should be placed
    :param keys_filepath: A string containing the filepath of the keys file containing all of the DATA448 IDs
    """
    keys = pd.read_csv(keys_filepath)

    for root, dirs, files in os.walk(zip_filepath):
        for file in files:
            if file.endswith('.zip'):
                filename = file.split('_')
                data448id = np.where(filename[0] == convert_name(keys.name.str), keys.data448id, 0)
                new_filename = str(data448id[0]) + "_" + filename[-1]
                filepath = os.sep.join([root, file])
                new_filepath = os.sep.join([output_path, root, new_filename])
                os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
                shutil.copy(filepath, new_filepath)
