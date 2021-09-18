import pandas as pd
from util import Encoder, EncoderException

KEY_PATH = '../../keys/Key.csv'
SURVEY_PATH = '../../data/Your_Impression_of_HCI__10_min_Header.csv'
EXPORT_PATH = '../../data/impression_survey.csv'
survey_df = pd.read_csv(SURVEY_PATH)


def convert_impression_survey():
    converted_survey_df = survey_df.drop(columns=['name'])
    for i, row in converted_survey_df.iterrows():
        try:
            encoder = Encoder(KEY_PATH)
            student_id = encoder.encode(row['id'])
            converted_survey_df.at[i, 'id'] = student_id
        except EncoderException:
            converted_survey_df.drop(i, inplace=True)
    converted_survey_df.to_csv(EXPORT_PATH, index=False)


if __name__ == "__main__":
    convert_impression_survey()
