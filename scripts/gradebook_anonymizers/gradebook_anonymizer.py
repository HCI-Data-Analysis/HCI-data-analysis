import os
import numpy as np
import pandas as pd

from util import data_cleaner
from util.encoder import Encoder


def gradebook_anonymize(gradebook_path, output_dir, filename, encoder: Encoder):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized gradebook specified in
    <gradebook_path>, using the keys file located in <keys_filepath>

    :param gradebook_path: A string containing the filepath of the gradebook to be anonymized
    :param output_dir: A string containing the path where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param keys_filepath: A string containing the filepath of the keys file containing all of the DATA448 IDs
    :param encoder: Instance of the encoder model that has been initialized with
    """

    file = pd.read_csv(gradebook_path)
    keys = pd.read_csv(keys_filepath)

    output_dir = os.path.join(output_dir, filename + ".csv")

    # file = data_cleaner.column_name_to_lower(file)

    headers = file.iloc[0:2]
    headers = headers.drop(["student", "id", "sis login id", "student number"], axis=1)
    headers.to_csv(output_dir)

    gradebook = file.iloc[2:len(file)]

    gradebook = gradebook.reset_index(drop=True)

    gradebook["data448id"] = np.where(gradebook.id == keys.id, keys.data448id, 0)
    gradebook = gradebook.drop(["student", "id", "sis login id", "student number"], axis=1)
    gradebook = gradebook.set_index("data448id")

    gradebook.to_csv(output_dir, mode='a', header=False)
