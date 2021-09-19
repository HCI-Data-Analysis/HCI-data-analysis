import pandas as pd
from schemas import TASurveySchema

KEY_PATH = '../../keys/Key.csv'
IMPRESSION_SURVEY_PATH = '../../data/341_TA_resources_survey_W2020T2_September_13_2021_12.36.csv'
IMPRESSION_EXPORT_PATH = '../../data/ta_survey.csv'


def convert_ta_survey(csv_path):
    survey_df = pd.read_csv(csv_path)
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


if __name__ == "__main__":
    survey = convert_ta_survey(IMPRESSION_SURVEY_PATH)
    survey.to_csv(IMPRESSION_EXPORT_PATH, index=False)