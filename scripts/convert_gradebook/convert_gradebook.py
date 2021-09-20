import pandas as pd
from util import Encoder, EncoderException
from schemas import GradeBookSchema

KEY_PATH = '../../keys/Key.csv'
GRADE_BOOK_CSV_PATH = '../../data/2021-09-13T1128_Grades-COSC_341_COSC_541_101_2020W.csv'
GRADE_BOOK_EXPORT_PATH = '../../data/grade_book.csv'


def convert_grade_book(csv_path):
    survey_df = pd.read_csv(csv_path)
    converted_survey_df = survey_df.drop(
        columns=[GradeBookSchema.STUDENT, GradeBookSchema.STUDENT_NUMBER, GradeBookSchema.SIS_LOGIN_ID])
    for i, row in converted_survey_df.iterrows():
        try:
            encoder = Encoder(KEY_PATH)
            student_id = encoder.encode(row[GradeBookSchema.ID])
            converted_survey_df.at[i, GradeBookSchema.ID] = student_id
        except EncoderException:
            converted_survey_df.drop(i, inplace=True)
    return converted_survey_df


if __name__ == "__main__":
    # Convert GradeBook
    survey = convert_grade_book(GRADE_BOOK_CSV_PATH)
    survey.to_csv(GRADE_BOOK_EXPORT_PATH, index=False)
