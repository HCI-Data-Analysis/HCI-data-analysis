import pandas as pd
from util import Encoder, EncoderException

KEY_PATH = '../../keys/Key.csv'
IMPRESSION_SURVEY_PATH = '../../data/Your_Impression_of_HCI__10_min_Header.csv'
IMPRESSION_EXPORT_PATH = '../../data/impression_survey.csv'
BACKGROUND_SURVEY_PATH = '../../data/341_Background_Survey_Header.csv'
BACKGROUND_EXPORT_PATH = '../../data/background_survey.csv'


def convert_survey(csv_path):
    survey_df = pd.read_csv(csv_path)
    converted_survey_df = survey_df.drop(columns=['name'])
    for i, row in converted_survey_df.iterrows():
        try:
            encoder = Encoder(KEY_PATH)
            student_id = encoder.encode(row['id'])
            converted_survey_df.at[i, 'id'] = student_id
        except EncoderException:
            converted_survey_df.drop(i, inplace=True)
    return converted_survey_df


if __name__ == "__main__":
    # Convert Impression Survey
    survey = convert_survey(IMPRESSION_SURVEY_PATH)
    survey.to_csv(IMPRESSION_EXPORT_PATH, index=False)

    # Convert Background Survey
    survey = convert_survey(BACKGROUND_SURVEY_PATH)
    survey.to_csv(BACKGROUND_EXPORT_PATH, index=False)