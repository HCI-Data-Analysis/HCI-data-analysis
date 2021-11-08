import re

from pandas import DataFrame, Series

from util import keep_latest_survey_attempt
from schemas import ModuleFeedbackSchema


def analyze_module_feedback(survey_df: DataFrame):
    processed_survey_df = preprocess_module_feedback_survey(survey_df)
    for question_col_name in ModuleFeedbackSchema.Questions.MC_SINGLE_ANSWER:
        plot_bar_graph(processed_survey_df[question_col_name])
    for question_col_name in ModuleFeedbackSchema.Questions.MC_MULTI_ANSWER:
        plot_bar_graph(processed_survey_df[question_col_name])


def preprocess_module_feedback_survey(survey_df: DataFrame) -> DataFrame:
    keep_last_attempt_df = keep_latest_survey_attempt(survey_df)
    ids_removed_from_headers = remove_id_from_question_titles(keep_last_attempt_df)
    return ids_removed_from_headers


def remove_id_from_question_titles(survey_df: DataFrame) -> DataFrame:
    def remove_id_prefix(col_name):
        regex = r'^([0-9]{7}: )'
        id_stripped_string = re.sub(regex, '', col_name)
        return id_stripped_string

    renamed_survey_df = survey_df.rename(remove_id_prefix, axis='columns')
    return renamed_survey_df


def preprocess_multiple_answer_data(data: Series) -> []:
    return []


def plot_bar_graph(data: Series, is_multiple_answer=False):
    if is_multiple_answer:
        data = preprocess_multiple_answer_data(data)

    freq = {}
    for value in data:
        freq[value] = freq.get(value, 0) + 1
    # TODO: plot the bar graph with the keys and values of the dict
