import os
import pandas as pd
import random

from schemas import GradeBookSchema, KeySchema


def generate_key(gradebook_path, output_dir, filename, seed=123456):
    """
    Outputs a file called <filename> to the the directory mentioned in <output_dir> that contains the generated
    5-digit random DATA448 IDs corresponding to each student id and name.

    :param gradebook_path: A string containing the filepath of the file to use for generating the master key file.
    :param output_dir: A string containing the path to the directory where the output keys file should be generated
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param seed: [optional] Specify a seed number to use for generating pseudorandom data448IDs. Defaults to 123456.
    """
    gradebook = pd.read_csv(gradebook_path)

    random.seed(seed)

    gradebook = gradebook.iloc[2:len(gradebook)]

    data448id = random.sample(range(10000, 99999), len(gradebook.index))
    gradebook[KeySchema.DATA448_ID] = data448id

    output_path = os.path.join(output_dir, filename + ".csv")

    gradebook.to_csv(
        output_path,
        columns=[KeySchema.STUDENT_NAME, KeySchema.CANVAS_ID, KeySchema.STUDENT_ID, KeySchema.DATA448_ID],
        index=False
    )
