from pandas import DataFrame

from schemas import GradeBookSchema
from util import Encoder, EncoderException


def convert_grade_book(survey_df: DataFrame, encoder: Encoder) -> DataFrame:
    converted_survey_df = survey_df.drop(
        columns=[GradeBookSchema.STUDENT, GradeBookSchema.STUDENT_NUMBER, GradeBookSchema.SIS_LOGIN_ID])
    for i, row in converted_survey_df.iterrows():
        try:
            student_id = encoder.encode(canvas_id=row[GradeBookSchema.ID])
            converted_survey_df.at[i, GradeBookSchema.ID] = student_id
        except EncoderException:
            converted_survey_df.drop(i, inplace=True)
    return converted_survey_df
