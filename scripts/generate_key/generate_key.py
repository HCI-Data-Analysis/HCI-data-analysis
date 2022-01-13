import pandas as pd
import random

import pandas as pd

from schemas import KeySchema


def generate_key(gradebook_path, output_path, seed=123456):
    """
    Outputs a file called <filename> to the the directory mentioned in <output_dir> that contains the generated
    5-digit random DATA448 IDs corresponding to each student id and name.

    :param gradebook_path: A string containing the filepath of the file to use for generating the master key file.
    :param output_path: A string containing the path to the key csv file (csv file extension should be included)
    :param seed: [optional] Specify a seed number to use for generating pseudorandom data448IDs. Defaults to 123456.
    """
    gradebook = pd.read_csv(gradebook_path)

    random.seed(seed)

    gradebook = gradebook.iloc[2:len(gradebook)]

    data448id = random.sample(range(1000000, 9999999), len(gradebook.index))
    gradebook[KeySchema.DATA448_ID] = data448id

    gradebook.to_csv(
        output_path,
        columns=[KeySchema.STUDENT_NAME, KeySchema.CANVAS_ID, KeySchema.STUDENT_ID, KeySchema.DATA448_ID],
        index=False
    )
