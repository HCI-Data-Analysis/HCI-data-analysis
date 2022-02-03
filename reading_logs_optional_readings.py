import pandas as pd

from scripts.reading_logs.optional_readings import analyze_optional_readings

IMPRESSIONS_SURVEY_1_PATH = 'data/anonymized/impression_survey1.csv'
IMPRESSIONS_SURVEY_2_PATH = 'data/anonymized/impression_survey2.csv'

RELEVANT_QUESTIONS = [
    'I think design and interaction is interesting.',
    'I think design and interaction is boring.',
    'I like to use design and interaction to solve problems.',
]

if __name__ == '__main__':
    impressions_survey_1_df = pd.read_csv(IMPRESSIONS_SURVEY_1_PATH)
    impressions_survey_2_df = pd.read_csv(IMPRESSIONS_SURVEY_2_PATH)

    for question in RELEVANT_QUESTIONS:
        print(question)
        analyze_optional_readings([impressions_survey_1_df, impressions_survey_2_df], question)

