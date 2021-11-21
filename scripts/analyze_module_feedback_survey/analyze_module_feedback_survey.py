import re

from pandas import DataFrame, Series

from schemas import ModuleFeedbackSchema
from util import keep_latest_survey_attempt

NAN = 'nan'


def compare_module_feedback(survey_1_df: DataFrame, survey_2_df: DataFrame):
    processed_survey_1_df = preprocess_module_feedback_survey(survey_1_df)
    processed_survey_2_df = preprocess_module_feedback_survey(survey_2_df)

    for question_col_name in ModuleFeedbackSchema.Questions.MC_SINGLE_ANSWER:
        print_freq_dict(
            processed_survey_1_df[question_col_name],
            question_col_name,
            compare_data=processed_survey_2_df[ModuleFeedbackSchema.Questions.convert_col_name(question_col_name)]
        )

    for question_col_name in ModuleFeedbackSchema.Questions.MC_MULTI_ANSWER:
        data_1 = preprocess_multiple_answer_data(processed_survey_1_df[question_col_name])
        data_2 = preprocess_multiple_answer_data(
            processed_survey_2_df[ModuleFeedbackSchema.Questions.convert_col_name(question_col_name)]
        )
        print_freq_dict(data_1, question_col_name, compare_data=data_2)


def analyze_module_feedback(survey_df: DataFrame):
    processed_survey_df = preprocess_module_feedback_survey(survey_df)

    for question_col_name in ModuleFeedbackSchema.Questions.MC_SINGLE_ANSWER:
        print_freq_dict(processed_survey_df[question_col_name], question_col_name)

    for question_col_name in ModuleFeedbackSchema.Questions.MC_MULTI_ANSWER:
        data = preprocess_multiple_answer_data(processed_survey_df[question_col_name])
        print_freq_dict(data, question_col_name)


def preprocess_module_feedback_survey(survey_df: DataFrame) -> DataFrame:
    """Preprocessing needed for module feedback surveys"""
    keep_last_attempt_df = keep_latest_survey_attempt(survey_df)
    ids_removed_from_headers = remove_id_from_question_titles(keep_last_attempt_df)
    return ids_removed_from_headers


def remove_id_from_question_titles(survey_df: DataFrame) -> DataFrame:
    """Removes question ids from the header strings of a DataFrame"""
    def remove_id_prefix(col_name):
        regex = r'^([0-9]{7}: )'
        id_stripped_string = re.sub(regex, '', col_name)
        return id_stripped_string

    renamed_survey_df = survey_df.rename(remove_id_prefix, axis='columns')
    return renamed_survey_df


def preprocess_multiple_answer_data(data: Series) -> []:
    """
    Breaks a Series containing strings of comma-separated-responses into a list of each response separately
    :param data: a Series object
    :return: a list of response strings
    """
    separated_values = []
    for value in data:
        if not value or str(value) == NAN:
            separated_values.append(NAN)
            continue
        current_values = value.replace('\\, ', ' & ').split(',')
        separated_values += current_values
    return separated_values


def create_answer_frequency_dict(data: iter, is_second=False) -> dict:
    """
    Creates a frequency dictionary to tally responses to a question
    :param data: an iterable (either Series or list)
    :param is_second: whether this is the second survey. This is to resolve minor wording changes between surveys
    :return: { str: int }
    """
    freq = {}
    for value in data:
        str_value = str(value)  # resolves the difference in dtypes from pandas
        str_value = ModuleFeedbackSchema.Questions.convert_answer_option(str_value) if is_second else str_value
        freq[str_value] = freq.get(str_value, 0) + 1

    if NAN in freq:
        freq['No Answer'] = freq.pop(NAN)

    return freq


def print_freq_dict(data: iter, question_text: str, compare_data: iter = None):
    """
    Prints the contents of the frequency dictionary into the terminal
    :param data: an iterable list of values (a Series or a list)
    :param question_text: the associated survey question text to be printed alongside the data
    :param compare_data: (optional) a second iterable to compare data to. If given, prints both side by side (data | compare_data) - qustion_text.
    """
    freq = create_answer_frequency_dict(data)
    freq_compare = create_answer_frequency_dict(compare_data, is_second=True) if compare_data else None
    print(f'"{question_text}" Answer Frequency')
    if freq_compare:
        merged_freq = merge_dict(freq, freq_compare)
        for answer_option, frequencies in merged_freq.items():
            f, f_c = frequencies
            print(f'\t{f} | {f_c}\t- {answer_option}')
    else:
        for answer_option, frequency in freq.items():
            print(f'\t{frequency}\t- {answer_option}')


def merge_dict(dict_1: dict, dict_2: dict) -> dict:
    """
    Merges two dictionaries into a single dictionary, but preserving the individual values from shared keys across dictionaries.
    { 'A': 1, 'B': 2 } merged with { 'A': 33, 'C': 44 } becomes { 'A': (1, 33), 'B': (2, NAN), 'C': (NAN, 44) }
    Where NAN refers to the constant at the top of this file.

    :param dict_1: The first dictionary, it's entries will be in index 0 of the tuple values.
    :param dict_2: The second dictionary, it's entries will be in index 1 of the tuple values.
    :return: { str: (int, int) }
    """
    new_dict = {}
    for key, value in dict_1.items():
        new_dict[key] = (value, NAN)
    for key, value in dict_2.items():
        if key in new_dict:
            val_1, _ = new_dict[key]
            new_dict[key] = (val_1, value)
        else:
            new_dict[key] = (NAN, value)
    return new_dict
