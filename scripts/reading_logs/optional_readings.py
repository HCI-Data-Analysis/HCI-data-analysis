import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

from schemas import CourseSchema
from scripts import prepare_data_for_clustering
from util import ReadingLogsData
from util.list import add_if_not_in, overlap


def get_cleaned_interest_data(first_survey: pd.DataFrame, second_survey: pd.DataFrame, survey_schema: pd.DataFrame):
    first_df_mod = prepare_data_for_clustering(first_survey, survey_schema).set_index('id')
    second_df_mod = prepare_data_for_clustering(second_survey, survey_schema).set_index('id')

    mutual_ids = overlap(list(first_df_mod.index), list(second_df_mod.index))
    print('-' * 50)
    print('Reporting N')
    print('First Survey n: ', len(list(first_df_mod.index)))
    print('Second Survey n: ', len(list(second_df_mod.index)))
    print('Mutual n: ', len(mutual_ids))

    first_df_mod = first_df_mod.loc[first_df_mod.index.isin(mutual_ids)]
    second_df_mod = second_df_mod.loc[second_df_mod.index.isin(mutual_ids)]

    # Sort by id so the each student's interest is the same position in both lists
    first_df_mod.sort_values(by='id', axis=0, inplace=True, na_position='first')
    second_df_mod.sort_values(by='id', axis=0, inplace=True, na_position='first')

    first_interest = first_df_mod['Interest']
    second_interest = second_df_mod['Interest']
    return first_interest, second_interest, mutual_ids


def change_in_interest_analysis(first_survey: pd.DataFrame, second_survey: pd.DataFrame, survey_schema: pd.DataFrame):
    first_interest, second_interest, mutual_ids = get_cleaned_interest_data(first_survey, second_survey, survey_schema)

    fi, si = list(first_interest), list(second_interest)
    inspect_data(fi, si)
    check_normality(fi, si)
    report_mean_std(fi, si)
    compare_interest(fi, si)
    plot_optional_reading_proportions([first_interest, second_interest], ['First', 'Second'], mutual_ids)


def inspect_data(first_interest: [], second_interest: []):
    fig, ax = plt.subplots()
    bins = np.linspace(-2, 2, 70)
    ax.hist(first_interest, bins=bins, color='r', alpha=0.5, label='First Impressions Survey')
    ax.hist(second_interest, bins=bins, color='b', alpha=0.5, label='Second Impressions Survey')
    ax.set_ylabel('Number of Students')
    ax.set_xlabel('HCI Interest')
    plt.legend()
    plt.show()


def check_normality(first_interest: [], second_interest: []):
    print('-' * 50)
    print('Check Normality of Data')
    print('H_0: The data is normally distributed\t', 'a = 0.05')
    print('Interpretation: p-value < 0.05 means we reject that this data follows a normal distribution')
    print('First Impressions Survey: ', test_normality(first_interest))
    print('Second Impressions Survey: ', test_normality(second_interest))

    # Check normality of difference between first and second surveys
    diff = [m1 - m2 for m1, m2 in zip(first_interest, second_interest)]
    print('Diff Impressions Survey: ', test_normality(diff))
    fig, ax = plt.subplots()
    bins = np.linspace(-2, 2, 70)
    ax.hist(diff, bins=bins, color='green', alpha=0.5, label='Diff Impressions Survey')
    ax.set_ylabel('Number of Students')
    ax.set_xlabel('Difference in HCI Interest (First - Second)')
    ax.set_title('')
    plt.legend()
    plt.show()


def test_normality(x: []):
    shapiro_wilks = scipy.stats.shapiro(x)
    return shapiro_wilks


def report_mean_std(first_interest: [], second_interest: []):
    print('-' * 50)
    print(f'First Mean: {np.mean(first_interest)} +/- {np.std(first_interest)}')
    print(f'Second Mean: {np.mean(second_interest)} +/- {np.std(second_interest)}')


def compare_interest(first_interest: [], second_interest: []):
    """
    H_0 = That the medians are equal
    H_a = two-sided (so just that their means are not equal
    """
    diff = [m1 - m2 for m1, m2 in zip(first_interest, second_interest)]
    wilcoxon = scipy.stats.wilcoxon(diff)
    print('-' * 50)
    print(wilcoxon)


def plot_optional_reading_proportions(interest_dfs: [pd.DataFrame], df_labels: [], mutual_ids: []):
    print('-' * 50)
    print('Optional Reading Analysis')
    print('Plot')
    reading_logs_data = ReadingLogsData()
    module_paragraphs_dict = reading_logs_data.get_module_paragraphs_dict()

    for interest_df, df_label in zip(interest_dfs, df_labels):
        pos_page_readers_dict = {}
        neg_page_readers_dict = {}
        neg_group_ids, pos_group_ids = student_interest_grouping(interest_df)
        print(' ' * 25 + '-' * 25)
        print(df_label)
        print('Num Students in Positive Group: ', len(pos_group_ids))
        print('Num Students in Negative Group: ', len(neg_group_ids))

        for module_num, pages in CourseSchema.OPTIONAL_PAGES.items():
            for page_num in pages:
                page_sections = module_paragraphs_dict[f'{module_num}']
                page_sections = page_sections[f'{page_num}']['sections']
                reader_ids = get_readers_for_page(module_num, page_num, allowed_ids=mutual_ids)

                pos_page_readers_dict[f'{module_num}-{page_num}'] = {
                    'title': list(page_sections.values())[0]['title'],
                    'readers': overlap(reader_ids, pos_group_ids)
                }

                neg_page_readers_dict[f'{module_num}-{page_num}'] = {
                    'title': list(page_sections.values())[0]['title'],
                    'readers': overlap(reader_ids, neg_group_ids)
                }

        plot_stacked_bar(pos_page_readers_dict, neg_page_readers_dict, df_label)


def plot_stacked_bar(pos_page_readers_dict: {}, neg_page_readers_dict: {}, df_label: str):
    interview_labels = []
    module_11_labels = []
    for module_num, page_nums in CourseSchema.OPTIONAL_PAGES.items():
        for page_num in page_nums:
            if module_num == 11:
                module_11_labels.append(f'{module_num}-{page_num}')
            else:
                interview_labels.append(f'{module_num}-{page_num}')

    figure_titles = ['Number of readers for each interview', 'Number of readers for each page in module 11']
    x_labels = ['Interview', 'Page']
    for label_set, fig_title, x_label in zip([interview_labels, module_11_labels], figure_titles, x_labels):
        pos_num_readers = []
        neg_num_readers = []

        all_pos_reader_for_label_set = []
        all_neg_reader_for_label_set = []

        for label in label_set:
            pos_num_readers.append(len(pos_page_readers_dict[label]['readers']))
            neg_num_readers.append(len(neg_page_readers_dict[label]['readers']))

            add_if_not_in(pos_page_readers_dict[label]['readers'], all_pos_reader_for_label_set)
            add_if_not_in(neg_page_readers_dict[label]['readers'], all_neg_reader_for_label_set)

        print(' ' * 25 + '-' * 25)
        print(f'Pos Group for {x_label}: ', len(all_pos_reader_for_label_set))
        print(f'Negative Group for {x_label}: ', len(all_neg_reader_for_label_set))

        width = 0.35
        fig, ax = plt.subplots()
        ax.bar(label_set, neg_num_readers, width, color='b', label='Negative Interest in HCI')
        ax.bar(label_set, pos_num_readers, width, color='r', bottom=neg_num_readers, label='Positive Interest in HCI')
        annotate_bars(ax)
        ax.set_ylabel('Number of Readers')
        ax.set_xlabel(f'{x_label}')
        ax.set_title(f'{fig_title} ({df_label})')
        ax.legend()
        plt.show()


def annotate_bars(ax):
    """Taken from https://www.pythoncharts.com/matplotlib/stacked-bar-charts-labels/"""
    # Let's put the annotations inside the bars themselves by using a
    # negative offset.
    y_offset = -5
    # For each patch (basically each rectangle within the bar), add a label.
    for bar in ax.patches:
        ax.text(
            # Put the text in the middle of each bar. get_x returns the start
            # so we add half the width to get to the middle.
            bar.get_x() + bar.get_width() / 2,
            # Vertically, add the height of the bar to the start of the bar,
            # along with the offset.
            bar.get_height() + bar.get_y() / 2 + y_offset,
            # This is actual value we'll show.
            round(bar.get_height()),
            # Center the labels and style them a bit.
            ha='center',
            color='w',
            weight='bold',
            size=6
        )


def get_readers_for_page(module_num: int, page_num: int, allowed_ids: [] = None):
    reading_logs_data = ReadingLogsData()
    reading_duration_dict = reading_logs_data.get_reading_duration_dict()

    page_reading_dict = reading_duration_dict[f'{module_num}-{page_num}']
    reader_data448_ids = [int(i) for i in page_reading_dict.index]

    return overlap(reader_data448_ids, allowed_ids) if allowed_ids else reader_data448_ids


def student_interest_grouping(interest_df) -> ([int], [int]):
    """Students with neutral interest are grouped into negative group as indifference is not positive"""
    negative_group = [i for i in interest_df.index if interest_df.at[i] <= 0]
    positive_group = [i for i in interest_df.index if interest_df.at[i] > 0]
    return negative_group, positive_group
