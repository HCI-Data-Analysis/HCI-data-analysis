import pandas as pd
import numpy as np

from schemas import KeySchema

KEY_CSV_PATH = '../keys/Key.csv'
key_df = pd.read_csv(KEY_CSV_PATH)


class EncoderException(Exception):
    pass


def encode(canvas_id: int = None, student_id: int = None) -> int:
    """
    Encodes a canvas_id or student_id into a data448_id. Only 1 of (canvas_id, student_id) is required to specify a
    student, since both should be unique, but if both are given, the function will try to find the student by
    canvas_id first, and then by student_id second

    :param canvas_id: a numeric canvas_id
    :param student_id: a numeric student_id
    :return: the data448_id corresponding to the specified student, as given in the key
    """
    if not canvas_id and not student_id:
        raise EncoderException('Neither a CanvasID nor a StudentID for the given student was specified.')

    data448_id = None
    if canvas_id:
        row = key_df.loc[key_df[KeySchema.CANVAS_ID] == canvas_id]
        data448_id = _retrieve_value_from_row(row, KeySchema.DATA448_ID)

    if student_id:
        row = key_df.loc[key_df[KeySchema.STUDENT_ID] == student_id]
        data448_id = _retrieve_value_from_row(row, KeySchema.DATA448_ID)

    if not data448_id:
        raise EncoderException('No students were found matching the given parameters.')

    return data448_id


def decode(data448_id: int) -> (int, int):
    """
    Decodes a data448ID back into a canvas_id and student_id

    :param data448_id: a numeric data448_id
    :return: a tuple of (canvas_id, student_id) corresponding to the specified student, as given in the key
    """
    row = key_df.loc[key_df[KeySchema.DATA448_ID] == data448_id]
    canvas_id = _retrieve_value_from_row(row, KeySchema.CANVAS_ID)
    student_id = _retrieve_value_from_row(row, KeySchema.STUDENT_ID)

    if not canvas_id and not student_id:
        raise EncoderException('No students were found matching the given parameters.')

    return canvas_id, student_id


def decode_to_canvas_id(data448_id: int) -> int:
    """Helper function to decode a data448_id into a canvas_id"""
    canvas_id, student_id = decode(data448_id)
    if not canvas_id:
        raise EncoderException('This student does not have a canvas_id')
    return canvas_id


def decode_to_student_id(data448_id: int) -> int:
    """Helper function to decode a data448_id into a student_id"""
    canvas_id, student_id = decode(data448_id)
    if not student_id:
        raise EncoderException('This student does not have a student_id')
    return student_id


def _retrieve_value_from_row(row, col_name):
    value = row[col_name].array
    if not value:
        pass
    elif len(value) == 1:
        return value[0]
    else:
        raise EncoderException('More than 1 student found matching the given parameters.')
