import os

import pandas as pd

from schemas import RawGradeBookSchema, KeySchema
from util import Encoder


def gradebook_anonymize(gradebook_path, output_dir, filename, encoder: Encoder):
    """Outputs a file to called <filename> to <output_filepath> that contains the anonymized gradebook specified in
    <gradebook_path>, using the keys file located in <keys_filepath>

    :param gradebook_path: A string containing the filepath of the gradebook to be anonymized
    :param output_dir: A string containing the path where the anonymized file should be placed
    :param filename: A string containing the name of the keys file to be generated. The .csv extension is automatically
    added, so if the file has to be named 'keys.csv', filename = 'keys'
    :param encoder: Instance of the encoder model that has been initialized with
    """

    file = pd.read_csv(gradebook_path)
    file = file.rename(columns={RawGradeBookSchema.CANVAS_ID: KeySchema.DATA448_ID})

    output_dir = os.path.join(output_dir, filename + ".csv")

    # Clean up some of the weird formatting of the gradebook
    headers = file.iloc[0:2]
    headers = headers.drop(
        columns=[RawGradeBookSchema.STUDENT_NAME, RawGradeBookSchema.STUDENT_ID, RawGradeBookSchema.SIS_LOGIN_ID]
    )
    # Now we retrieve the data from the file
    gradebook = file.iloc[2:len(file)]
    gradebook[KeySchema.DATA448_ID] = gradebook[KeySchema.DATA448_ID].map(
        lambda canvas_id: encoder.encode(canvas_id=canvas_id)
    )
    gradebook = gradebook.drop(
        columns=[RawGradeBookSchema.STUDENT_NAME, RawGradeBookSchema.STUDENT_ID, RawGradeBookSchema.SIS_LOGIN_ID]
    )

    # There are multiple header rows in this dataframe, so we write the 2 extra header rows to a csv first
    headers.to_csv(output_dir, index=False)
    # Append the anonymized gradebook data to the previously written headers to make a completely anonymized gradebook
    gradebook.to_csv(output_dir, mode='a', header=False, index=False)
