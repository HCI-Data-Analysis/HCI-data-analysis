from pandas import DataFrame
from util import Encoder, EncoderException
from schemas import SurveySchema


def convert_survey(survey_df: DataFrame, encoder: Encoder) -> DataFrame:
    converted_survey_df = survey_df.drop(columns=[SurveySchema.NAME])
    for i, row in converted_survey_df.iterrows():
        try:
            student_id = encoder.encode(canvas_id=row[SurveySchema.ID])
            converted_survey_df.at[i, SurveySchema.ID] = student_id
        except EncoderException:
            converted_survey_df.drop(i, inplace=True)
    return converted_survey_df
