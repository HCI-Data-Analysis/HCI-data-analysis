import os
import numpy as np
import pandas as pd


from scripts.utils import data_cleaner


def gradebook_anonymize(gradebook_filepath, output_path, filename, keys_filepath):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized gradebook specified in
        <gradebook_filepath>, using the keys file located in <keys_filepath>
        :param gradebook_filepath: A string containing the filepath of the gradebook to be anonymized
        :param output_path: A string containing the path where the anonymized file should be placed
        :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
        added, so if the file has to be named 'keys.csv', filename = 'keys'
        :param keys_filepath: A string containing the filepath of the keys file containing all of the DATA448 IDs
        """

    file = pd.read_csv(gradebook_filepath)
    keys = pd.read_csv(keys_filepath)

    output_path = os.path.join(output_path, filename + ".csv")

    data_cleaner.column_name_to_lower(file)

    headers = file.iloc[0:2]
    headers = headers.drop(["student", "id", "sis login id", "student number"], axis=1)
    headers.to_csv(output_path)

    gradebook = file.iloc[2:len(file)]

    gradebook = gradebook.reset_index(drop=True)

    gradebook["data448id"] = np.where(gradebook.id == keys.id, keys.data448id, 0)
    gradebook = gradebook.drop(["student", "id", "sis login id", "student number"], axis=1)
    gradebook = gradebook.set_index("data448id")

    gradebook.to_csv(output_path, mode='a', header=False)

