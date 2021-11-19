import pandas as pd

from schemas import KeySchema


class EncoderException(Exception):
    pass


class Encoder:
    def __init__(self, key_path):
        self.key_df = pd.read_csv(key_path)

    def encode(self, canvas_id: int = None, student_id: int = None, student_name: str = None) -> int:
        """
        Encodes a canvas_id, student_id, student_name into a data448_id. Only 1 of (canvas_id, student_id, student_name)
        is required to specify a student, since both should be unique, but if more than one is given, the function will
        try to find the student by canvas_id first, then by student_id second, and the student_name third

        :param canvas_id: a numeric canvas_id
        :param student_id: a numeric student_id
        :param student_name: a string type student_name
        :return: the data448_id corresponding to the specified student, as given in the key
        """
        if not canvas_id and not student_id and not student_name:
            raise EncoderException('Neither a CanvasID, StudentID, nor a Student Name '
                                   'for the given student was specified.')

        data448_id = None
        if canvas_id:
            row = self.key_df.loc[self.key_df[KeySchema.CANVAS_ID] == canvas_id]
            data448_id = self._retrieve_value_from_row(row, KeySchema.DATA448_ID)

        if not data448_id and student_id:
            row = self.key_df.loc[self.key_df[KeySchema.STUDENT_ID] == student_id]
            data448_id = self._retrieve_value_from_row(row, KeySchema.DATA448_ID)

        if not data448_id and student_name:
            row = self.key_df.loc[self.key_df[KeySchema.STUDENT_NAME] == student_name]
            data448_id = self._retrieve_value_from_row(row, KeySchema.DATA448_ID)

        if not data448_id and canvas_id != 0:
            print(canvas_id)
            raise EncoderException('No students were found matching the given parameters.')

        return int(data448_id)

    def decode(self, data448_id: int) -> (int, int):
        """
        Decodes a data448ID back into a canvas_id and student_id

        :param data448_id: a numeric data448_id
        :return: a tuple of (canvas_id, student_id) corresponding to the specified student, as given in the key
        """
        row = self.key_df.loc[self.key_df[KeySchema.DATA448_ID] == data448_id]
        canvas_id = self._retrieve_value_from_row(row, KeySchema.CANVAS_ID)
        student_id = self._retrieve_value_from_row(row, KeySchema.STUDENT_ID)

        if not canvas_id and not student_id:
            raise EncoderException('No students were found matching the given parameters.')

        return canvas_id, student_id

    def decode_to_canvas_id(self, data448_id: int) -> int:
        """Helper function to decode a data448_id into a canvas_id"""
        canvas_id, _ = self.decode(data448_id)
        if not canvas_id:
            raise EncoderException('This student does not have a canvas_id')
        return canvas_id

    def decode_to_student_id(self, data448_id: int) -> int:
        """Helper function to decode a data448_id into a student_id"""
        _, student_id = self.decode(data448_id)
        if not student_id:
            raise EncoderException('This student does not have a student_id')
        return student_id

    def _retrieve_value_from_row(self, row, col_name):
        value = row[col_name].array
        if not value:
            pass
        elif len(value) == 1:
            return value[0]
        else:
            raise EncoderException('More than 1 student found matching the given parameters.')
