import json
import os

import matplotlib.patches as pch
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats
import seaborn as sns

from schemas import GradeBookSchema
from scripts import get_quiz_object
from util import get_quiz_id_from_file_name

QUIZ_PATH = "../../data/api/canvas/quizzes"
PARENT_PATH = "../../data/api/canvas"


def course_performance_analysis(gradebook, QUIZSCOREJSON_PATH, QUIZ_OBJECT_PATH):
    sns.color_palette('bright')

    data448_ids = gradebook[GradeBookSchema.STUDENT_ID]
    quiz_ids = []
    final_score = gradebook[GradeBookSchema.FINAL_SCORE]

    overall_pre_test = gradebook[GradeBookSchema.PRE_TEST_SCORE]
    overall_post_test = gradebook[GradeBookSchema.POST_TEST_SCORE]

    df_first_attempt = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'score', 'time', 'possible_points']
    )
    df_student_grade_first_attempt = pd.DataFrame(
        columns=['DATA448_ID', 'total_score', 'final_score', 'first_attempt_final_score',
                 'overall_quiz_score', 'first_attempt_quiz_score']
    )
    df_average_student_attempts = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'attempt', 'final_score']
    )
    df_submission_type = pd.DataFrame(
        columns=['QUIZ_ID', 'quiz_title', 'submission_type', 'total_score']
    )

    # distinguish submission type
    for file in os.listdir(QUIZ_OBJECT_PATH):
        if file.endswith('.json'):
            file_quiz_id = get_quiz_id_from_file_name(file)
            quiz_object_path = get_quiz_object(file_quiz_id, QUIZ_OBJECT_PATH)
            with open(quiz_object_path, 'r') as quiz_object:
                file = quiz_object.read()
                json_file = json.loads(file)
                if json_file:
                    quiz_title = json_file[0]['title'].lower()
                    points_possible = json_file[0]['points_possible']
                    if 'pre-test' in quiz_title:
                        submission_type = {
                            'QUIZ_ID': file_quiz_id,
                            'quiz_title': quiz_title,
                            'submission_type': 'Pre-Test',
                            'total_score': points_possible
                        }
                    elif 'post-test' in quiz_title:
                        submission_type = {
                            'QUIZ_ID': file_quiz_id,
                            'quiz_title': quiz_title,
                            'submission_type': 'Post-Test',
                            'total_score': points_possible
                        }
                    else:
                        submission_type = {
                            'QUIZ_ID': file_quiz_id,
                            'quiz_title': quiz_title,
                            'submission_type': 'Survey',
                            'total_score': points_possible
                        }
                    df_submission_type = df_submission_type.append(submission_type, ignore_index=True)

    QUIZ_POINTS_POSSIBLE = "quiz_points_possible"
    FIRST_ATTEMPT_FINAL_SCORE = 'first_attempt_final_score'
    FINAL_SCORE = 'final_score'
    COMBINED_PRE_POST_WORTH = 40

    # Get first attempt only quiz mark out of JSON files
    number_of_quizzes = 0
    for i in os.listdir(QUIZSCOREJSON_PATH):
        if i.endswith('.json'):
            number_of_quizzes += 1
            full_path = os.path.join(QUIZSCOREJSON_PATH, i)
            with open(full_path, 'r') as f:
                gradebook = f.read()
                json_file = json.loads(gradebook)
                if json_file:
                    if json_file[0][QUIZ_POINTS_POSSIBLE] > 0:
                        quiz_ids.append(json_file[0]['quiz_id'])
                for json_block in json_file:
                    if json_block[QUIZ_POINTS_POSSIBLE] > 0:
                        student_average_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'attempt': json_block['attempt'],
                            'final_score': json_block['kept_score'] / json_block[QUIZ_POINTS_POSSIBLE] * 100
                        }
                        df_average_student_attempts = df_average_student_attempts.append(student_average_attempt_data,
                                                                                         ignore_index=True)
                        if json_block['attempt'] > 1:
                            for previous_json_block in json_block['previous_submissions']:
                                if previous_json_block['attempt'] == 1:
                                    json_block = previous_json_block
                        student_first_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'score': json_block['score'],
                            'time': json_block['time_spent'],
                            'possible_points': json_block[QUIZ_POINTS_POSSIBLE]
                        }
                        df_first_attempt = df_first_attempt.append(student_first_attempt_data, ignore_index=True)

    # df_first_attempt = remove_survey_from_df(df_first_attempt, df_submission_type)
    df_average_student_attempts = remove_survey_from_df(df_average_student_attempts, df_submission_type)
    quiz_ids = remove_survey_from_list(quiz_ids, df_submission_type)

    for index, data448_id in enumerate(data448_ids):
        df_student_first_attempts = df_first_attempt.loc[df_first_attempt['DATA448_ID'] == data448_id]

        total_score = df_student_first_attempts['score'].sum()
        final_score_percentage = final_score[index]

        pre_test_grade = overall_pre_test[index]
        post_test_grade = overall_post_test[index]
        
        overall_quiz_grade = (pre_test_grade + post_test_grade) / total_quiz_worth
        first_attempt_final_score_percentage = (total_score / total_possible_points) * COMBINED_PRE_POST_WORTH

        first_attempt_final_score_percentage = (total_score / total_quiz_possible_score) * total_quiz_worth
        first_attempt_final_score = final_score_percentage - (
                pre_test_grade + post_test_grade) + first_attempt_final_score_percentage
        first_attempt_quiz_score = total_score / total_quiz_possible_score * 100

        df_student_grade_first_attempt = df_student_grade_first_attempt.append({
            'DATA448_ID': data448_id,
            'total_score': total_score,
            'final_score': final_score,
            'first_attempt_final_score': first_attempt_final_score,
            'overall_quiz_score': overall_quiz_grade,
            'first_attempt_quiz_score': first_attempt_quiz_score
        }, ignore_index=True)

    # First attempt only score mean and std
    mean = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE].mean()
    standard_dev = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE].std()
    quantile_25percent = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE].quantile(.25)
    median = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE].median()
    quantile_75percent = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE].quantile(.75)

    # Actual Score mean and std
    current_mean = final_score.mean()
    current_standard_dev = final_score.std()

    # First time quiz score mean and std
    first_time_quiz_mean = df_student_grade_first_attempt['first_attempt_quiz_score'].mean()
    first_time_quiz_std = df_student_grade_first_attempt['first_attempt_quiz_score'].std()

    # Overall Quiz Score mean and std
    quiz_mean = df_student_grade_first_attempt['overall_quiz_score'].mean()
    quiz_std = df_student_grade_first_attempt['overall_quiz_score'].std()

    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_retrieve_avg, w_2020_retrieve_std = 90.80, 10.5
    w_2020_calculated_avg, w_2020_calculated_std = current_mean, current_standard_dev
    w_2020_first_attempt_avg, w_2020_first_attempt_std = mean, standard_dev

    winter_averages = [w_2016_avg, w_2017_avg, w_2018_avg, w_2019_avg, w_2020_retrieve_avg, w_2020_calculated_avg,
                       w_2020_first_attempt_avg]
    winter_deviations = [w_2016_std, w_2017_std, w_2018_std, w_2019_std, w_2020_retrieve_std, w_2020_calculated_std,
                         w_2020_first_attempt_std]
    winter_labels = ['W2016', 'W2017', 'W2018', 'W2019', 'W2020', 'C W2020', 'F 2020']

    # print out the statistics significant value of the overall final score.
    print('25% quantile: ' + str(final_score.quantile(.25)), ' Median: ' + str(final_score.median()),
          ' 75% quantile: ' + str(final_score.quantile(.75)), ' Mean: ' + str(current_mean),
          ' Standard Deviation: ' + str(current_standard_dev))

    # print out the statistics significant value of the first attempt final score.
    print('25% quantile: ' + str(quantile_25percent), ' Median: ' + str(median),
          ' 75% quantile: ' + str(quantile_75percent), ' Mean: ' + str(mean),
          ' Standard Deviation: ' + str(standard_dev))

    # 1) Histogram comparison plot for Actual score and First attempt only score
    fig, (ax1) = plt.subplots(1)
    data_graph_colors = ['b', 'r']
    overall_mean_std = "Overall Score\nMean: " + str(round(current_mean, 2)) + "  " + "Std Dev: " + str(
        round(current_standard_dev, 2))
    first_attempt_mean_std = "First Attempt Score\nMean: " + str(round(mean, 2)) + "  " + "Std Dev: " + str(
        round(standard_dev, 2))
    for index, data in enumerate([final_score, df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE]]):
        sns.histplot(data, kde=True, bins=30, line_kws={'linewidth': 1}, color=data_graph_colors[index], ax=ax1).set(
            title='Overall Score vs First Attempt Score',
            xlabel='Grade',
            ylabel='Number of Students')
    plt.text(42, 18, overall_mean_std)
    plt.text(42, 15, first_attempt_mean_std)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    score_legend = pch.Patch(color=data_graph_colors[0], label='Overall Score')
    first_attempt_legend = pch.Patch(color=data_graph_colors[1], label='First Attempt Score')
    ax1.legend(handles=[score_legend, first_attempt_legend])
    fig.tight_layout()
    plt.savefig(f'data/graphs/overall_vs_first_attempt.png')
    plt.close()

    # 1b) Histogram comparison plot for Overall quiz score and First attempt only quiz score
    fig, (ax1) = plt.subplots(1)
    data_graph_colors = ['b', 'r']
    overall_mean_std = "Overall Quiz Score\nMean: " + str(round(quiz_mean, 2)) + "  " + "Std Dev: " + str(
        round(quiz_std, 2))
    first_attempt_mean_std = "First Attempt Quiz Score\nMean: " + str(round(first_time_quiz_mean, 2)) + "  " + "Std Dev: " + str(
        round(first_time_quiz_std, 2))
    for index, data in enumerate([final_score, df_student_grade_first_attempt['first_attempt_quiz_score']]):
        sns.histplot(data, kde=True, bins=30, line_kws={'linewidth': 1}, color=data_graph_colors[index], ax=ax1).set(
            title='Overall Quiz Score vs First Attempt Quiz Score',
            xlabel='Grade',
            ylabel='Number of Students')
    plt.text(42, 18, overall_mean_std)
    plt.text(42, 15, first_attempt_mean_std)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    score_legend = pch.Patch(color=data_graph_colors[0], label='Overall Quiz Score')
    first_attempt_legend = pch.Patch(color=data_graph_colors[1], label='First Attempt Quiz Score')
    ax1.legend(handles=[score_legend, first_attempt_legend])
    fig.tight_layout()
    plt.savefig(f'data/graphs/overall_vs_first_attempt_quiz.png')
    plt.close()

    # 2) Histogram comparison plot for Actual score and First attempt only score
    fig, (ax1) = plt.subplots(1)
    sns.histplot(final_score, kde=True, bins=30, line_kws={'linewidth': 1}, ax=ax1).set(
        title='Overall Final Score',
        xlabel='Grade',
        ylabel='Number of Students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    fig.tight_layout()
    plt.savefig(f'data/graphs/course_performance.png')
    plt.close()

    # 3) Mean and Standard Deviation graph
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.barh(winter_labels, winter_averages, xerr=winter_deviations, capsize=3)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_xlim([40, 110])
    ax1.set_title('Yearly Winter Term Grade History')

    ax2.errorbar(winter_labels, winter_averages, yerr=winter_deviations, capsize=4)
    ax2.set_yticks(range(60, 105, 5))
    fig.tight_layout()
    plt.savefig(f'data/graphs/mean_and_standard_deviation.png')
    plt.close()

    # 4) Students grades to attempts taken for each quiz
    for quiz_id in quiz_ids:
        students_per_quiz = df_average_student_attempts.loc[df_average_student_attempts['QUIZ_ID'] == quiz_id]

        quiz_attempt_grade_data = {
            'final_score': list(students_per_quiz[FINAL_SCORE]),
            'attempts': list(students_per_quiz['attempt'])
        }

        temp_mean = "Mean: " + str(round(students_per_quiz[FINAL_SCORE].mean(), 2))
        temp_std = "Std Dev: " + str(round(students_per_quiz[FINAL_SCORE].std(), 2))
        df = pd.DataFrame(quiz_attempt_grade_data)

        fig = sns.jointplot(x='final_score', y='attempts', kind='reg', data=df)
        fig.set_axis_labels('Final Score', 'Attempts')
        fig.ax_marg_x.set_xlim(0, 110)
        fig.ax_marg_y.set_ylim(0, 4)
        plt.text(5, 4, temp_mean)
        plt.text(5, 3.7, temp_std)

        quiz_name = df_submission_type.loc[df_submission_type['QUIZ_ID'] == str(quiz_id), "quiz_title"].iloc[0]
        out_of_x = df_submission_type.loc[df_submission_type['QUIZ_ID'] == str(quiz_id), "total_score"].iloc[0]
        fig.figure.suptitle(f'Final Score (out of {out_of_x}) vs Attempts Taken For {quiz_name}')
        fig.figure.tight_layout()
        plt.savefig(f'data/graphs/final_score_vs_attempts_{quiz_name}.png')
        plt.close()

    # Wilcoxon signed-rank test exploration - overall
    print(scipy.stats.shapiro(final_score))
    print(scipy.stats.shapiro(df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE]))
    scipy.stats.probplot(final_score, dist="norm", plot=plt)
    plt.title("Overall Final Score Q-Q Plot")
    plt.savefig("data/graphs/overall_QQ.png")
    plt.close()
    scipy.stats.probplot(df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE], dist="norm", plot=plt)
    plt.title("First Attempt Final Score Q-Q Plot")
    plt.savefig("data/graphs/first_attempt_QQ.png")
    plt.close()
    final_score = final_score
    first_score = df_student_grade_first_attempt[FIRST_ATTEMPT_FINAL_SCORE]
    difference_score = final_score - first_score
    wilcoxon = scipy.stats.wilcoxon(final_score, first_score)
    print(wilcoxon)

    plt.show()

    # Wilcoxon signed-rank test exploration - quiz
    print(scipy.stats.shapiro(df_student_grade_first_attempt['overall_quiz_score']))
    print(scipy.stats.shapiro(df_student_grade_first_attempt['first_attempt_quiz_score']))
    scipy.stats.probplot(final_score, dist="norm", plot=plt)
    plt.title("Overall Quiz Score Q-Q Plot")
    plt.savefig("data/graphs/quiz_QQ.png")
    plt.close()
    scipy.stats.probplot(df_student_grade_first_attempt['first_attempt_quiz_score'], dist="norm", plot=plt)
    plt.title("First Attempt Quiz Score Q-Q Plot")
    plt.savefig("data/graphs/first_attempt_quiz_QQ.png")
    plt.close()
    quiz_final_score = df_student_grade_first_attempt['overall_quiz_score']
    first_quiz_score = df_student_grade_first_attempt['first_attempt_final_score']
    # difference_score = quiz_final_score - first_quiz_score
    wilcoxon = scipy.stats.wilcoxon(quiz_final_score, first_quiz_score)
    print(wilcoxon)

    plt.show()


def remove_survey_from_df(df, submission_type_df):
    for index, row in submission_type_df.iterrows():
        if row["submission_type"] == "Survey":
            quiz_id = row["QUIZ_ID"]
            df = df.drop(df[df['QUIZ_ID'] == float(quiz_id)].index)
    return df


def remove_survey_from_list(lst, submission_type_df):
    for index, row in submission_type_df.iterrows():
        if row["submission_type"] == "Survey":
            quiz_id = int(row["QUIZ_ID"])
            if quiz_id in lst:
                lst.remove(quiz_id)
    return lst
