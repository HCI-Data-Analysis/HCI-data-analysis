from pandas import DataFrame
from schemas import TASurveySchema
from util import Encoder


def convert_ta_survey(survey_df: DataFrame, encoder: Encoder) -> DataFrame:
    converted_survey_df = survey_df.drop(columns=[
        TASurveySchema.STATUS,
        TASurveySchema.IP_ADDRESS,
        TASurveySchema.RESPONSE_ID,
        TASurveySchema.RECIPIENT_FIRST_NAME,
        TASurveySchema.RECIPIENT_LAST_NAME,
        TASurveySchema.RECIPIENT_EMAIL,
        TASurveySchema.EXTERNAL_REFERENCE,
        TASurveySchema.LATITUDE,
        TASurveySchema.LONGITUDE,
        TASurveySchema.DISTRIBUTION_CHANNEL
    ]).drop(labels=[0, 1], axis=0)
    return converted_survey_df
