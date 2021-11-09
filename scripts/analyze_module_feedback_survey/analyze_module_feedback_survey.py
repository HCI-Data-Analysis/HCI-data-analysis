import re
from textwrap import wrap

import matplotlib
from matplotlib import pyplot as plt
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
        plot_bar_graph(processed_survey_df[question_col_name], question_col_name)

    for question_col_name in ModuleFeedbackSchema.Questions.MC_MULTI_ANSWER:
        data = preprocess_multiple_answer_data(processed_survey_df[question_col_name])
        print_freq_dict(data, question_col_name)
        plot_bar_graph(data, question_col_name)


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
    separated_values = []
    for value in data:
        # FIXME: this could be better, honestly
        if not value or str(value) == NAN:
            separated_values.append(NAN)
            continue
        current_values = value.replace('\\, ', ' & ').split(',')
        separated_values += current_values
    return separated_values


def create_answer_frequency_dict(data: iter, is_second=False):
    freq = {}
    for value in data:
        str_value = str(value)  # resolves the difference in dtypes from pandas
        temp = str_value
        str_value = ModuleFeedbackSchema.Questions.convert_answer_option(str_value) if is_second else str_value
        if temp != str_value:
            a = 7
        freq[str_value] = freq.get(str_value, 0) + 1

    if NAN in freq:
        freq['No Answer'] = freq.pop(NAN)

    return freq


def set_plot_settings():
    font = {
        'family': 'sans-serif',
        'weight': 'normal',
        'size': 10,
    }
    matplotlib.rc('font', **font)

    axes = {
        'titlesize': 10,
    }
    matplotlib.rc('axes', **axes)


def print_freq_dict(data: iter, question_text: str, compare_data: iter = None):
    freq = create_answer_frequency_dict(data)
    freq_compare = create_answer_frequency_dict(compare_data, is_second=True)
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


def plot_bar_graph(data: iter, question_text: str):
    set_plot_settings()
    freq = create_answer_frequency_dict(data)

    plt.bar(list(freq.keys()), list(freq.values()))
    plt.xlabel("Answer Option")
    plt.title("\n".join(wrap(f"'{question_text}'")))
    # plt.subplots_adjust(top=0.65)
    # plt.setp(plt.gca().get_xticklabels(), fontsize=10, rotation=45)
    plt.xticks(rotation=-45)
    plt.show()
