import os
import pandas as pd
import random


def generate_key(sample_filepath, output_path, filename):
    """Outputs a file called <filename> to the the directory mentioned in <output_path> that contains the generated
    5-digit random DATA448 IDs corresponding to each student id and name.

    :param sample_filepath: A string containing the filepath of the file to use for generating the master keys file
    :param output_path: A string containing the path where the output keys file should be generated
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    """
    sample_file = pd.read_csv(sample_filepath)

    random.seed(123456)
    data448id = random.sample(range(10000, 99999), len(sample_file.index))
    sample_file['data448id'] = data448id

    output_path = os.path.join(output_path, filename + ".csv")

    sample_file.to_csv(output_path, columns=["id", "name", "data448id"])

    print(sample_file)
