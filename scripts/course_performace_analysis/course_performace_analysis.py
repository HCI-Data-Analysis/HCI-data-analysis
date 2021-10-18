import json
import os
from collections import defaultdict

import matplotlib.patches as pch
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def course_performance_with_first_attempt_analysis(GRADEBOOK_PATH, QUIZSCOREJSON_PATH):
    sns.color_palette('bright')
    file = pd.read_csv(GRADEBOOK_PATH)
    data448_ids = file['ID']
    final_score = file['Overall Final Score']

    quiz_data = {}

    # Get first attempt only quiz mark out of JSON files
    number_of_quizzes = 0
    for i in os.listdir(QUIZSCOREJSON_PATH):
        if i.endswith('.json'):
            number_of_quizzes += 1
            full_path = os.path.join(QUIZSCOREJSON_PATH, i)
            with open(full_path, 'r') as f:
                file = f.read()
                json_file = json.loads(file)
                if json_file:
                    quiz_data[json_file[0]['quiz_id']] = {
                        'total_time_spent': 0,
                        'average_time_spent': 0,
                        'highest_score': 0,
                        'lowest_score': json_file[0]['quiz_points_possible'],
                        'users_quiz_data': [],
                        'attempt_counters': defaultdict(int),
                        'time_per_attempt': defaultdict(int),
                        'total_points': json_file[0]['quiz_points_possible']
                    }
                total_submissions = 0
                for json_block in json_file:
                    user_id = json_block['user_id']
                    time_spent = json_block['time_spent']
                    score = json_block['kept_score']
                    attempt = json_block['attempt']
                    quiz_data[json_file[0]['quiz_id']]['total_time_spent'] += time_spent
                    quiz_data[json_file[0]['quiz_id']]['average_time_spent'] += time_spent
                    if score < quiz_data[json_file[0]['quiz_id']]['lowest_score']:
                        quiz_data[json_file[0]['quiz_id']]['lowest_score'] = score
                    if score > quiz_data[json_file[0]['quiz_id']]['highest_score']:
                        quiz_data[json_file[0]['quiz_id']]['highest_score'] = score
                    quiz_data[json_file[0]['quiz_id']]['time_per_attempt'][attempt] += time_spent
                    quiz_data[json_file[0]['quiz_id']]['attempt_counters'][attempt] += 1
                    quiz_data[json_file[0]['quiz_id']]['users_quiz_data'].append({
                        'user_id': user_id,
                        'time_spent': time_spent,
                        'score': score,
                        'attempt': attempt
                    })
                    total_submissions += 1
                if json_file:
                    quiz_data[json_file[0]['quiz_id']]['average_time_spent'] /= total_submissions

    mean = final_score.mean()
    standard_dev = final_score.std()
    quantile_25percent = final_score.quantile(.25)
    median = final_score.median()
    quantile_75percent = final_score.quantile(.75)

    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_retrieve_avg, w_2020_retrieve_std = 90.80, 10.5
    w_2020_calculated_avg, w_2020_calculated_std = mean, standard_dev

    winter_averages = [w_2016_avg, w_2017_avg, w_2018_avg, w_2019_avg, w_2020_retrieve_avg, w_2020_calculated_avg]
    winter_deviations = [w_2016_std, w_2017_std, w_2018_std, w_2019_std, w_2020_retrieve_std, w_2020_calculated_std]
    winter_labels = ['W2016', 'W2017', 'W2018', 'W2019', 'W2020', 'H W2020']

    print('25% quantile: ' + str(quantile_25percent), ' Median: ' + str(median),
          ' 75% quantile: ' + str(quantile_75percent), ' Mean: ' + str(mean),
          ' Standard Deviation: ' + str(standard_dev))

    # 1) Mean and Standard Deviation graph
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.barh(winter_labels, winter_averages, xerr=winter_deviations, capsize=3)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_xlim([40, 110])
    ax1.set_title('Yearly Winter Term Grade History')

    ax2.errorbar(winter_labels, winter_averages, yerr=winter_deviations, capsize=4)
    ax2.set_yticks(range(60, 105, 5))
    fig.tight_layout()

    # 2) Density plot graph for overall score
    fig, (ax1) = plt.subplots(1)
    sns.histplot(final_score, kde=True, bins=30, line_kws={'linewidth': 1}).set(
        title='Overall Course performance',
        xlabel='Grade',
        ylabel='Number of Students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    fig.tight_layout()

    # 3) Number of finishing attempts per quiz
    data = {
        'attempt_number': [],
        'number_of_students': []
    }
    for quiz_id, quiz in quiz_data.items():
        for attempt_number, number_of_students in quiz['attempt_counters'].items():
            data['attempt_number'].append(attempt_number)
            data['number_of_students'].append(number_of_students)
    df = pd.DataFrame(data)
    fig, (ax1) = plt.subplots(1)
    sns.boxplot(x='attempt_number', y='number_of_students', data=df, ax=ax1).set(
        title='Finishing Attempts Per Quiz',
        xlabel='Attempt Number',
        ylabel='Number of Students'
    )
    fig.tight_layout()

    # 4) Students grades to average attempts taken
    final_score_attempts = {
        'user_id': list(data448_ids),
        'final_score': list(final_score)
    }
    id_to_attempts = defaultdict(int)
    for quiz_id, quiz in quiz_data.items():
        for user_quiz_data in quiz['users_quiz_data']:
            id_to_attempts[user_quiz_data['user_id']] += user_quiz_data['attempt'] / len(quiz_data)
    final_score_attempt_data = []
    for user_id in data448_ids:
        final_score_attempt_data.append(id_to_attempts[user_id])
    final_score_attempts['average_attempts_per_quiz'] = final_score_attempt_data
    df = pd.DataFrame(final_score_attempts)
    fig = sns.jointplot(x='final_score', y='average_attempts_per_quiz', kind='reg', data=df)
    fig.set_axis_labels('Final Score', 'Average Attempts Per Quiz')
    fig.figure.suptitle('Final Score vs Average Attempts Per Quiz')
    fig.figure.tight_layout()

    def outliers(tdf, feature):
        Q1 = tdf[feature].quantile(0.25)
        Q3 = tdf[feature].quantile(0.75)
        upper_limit = Q3
        lower_limit = Q1
        return upper_limit, lower_limit

    # 5) Students grades to average time taken
    final_score_time = {
        'user_id': list(data448_ids),
        'final_score': list(final_score)
    }
    id_to_attempts = defaultdict(int)
    for quiz_id, quiz in quiz_data.items():
        for user_quiz_data in quiz['users_quiz_data']:
            id_to_attempts[user_quiz_data['user_id']] += user_quiz_data['time_spent'] / len(quiz_data)
    final_score_time_data = []
    for user_id in data448_ids:
        final_score_time_data.append(id_to_attempts[user_id])
    final_score_time['average_time_per_quiz'] = final_score_time_data
    df = pd.DataFrame(final_score_time)
    upper, lower = outliers(df, 'average_time_per_quiz')
    new_df = df[(df['average_time_per_quiz'] > lower) & (df['average_time_per_quiz'] < upper)]
    fig = sns.jointplot(x='final_score', y='average_time_per_quiz', kind='reg', data=new_df)
    fig.set_axis_labels('Final Score', 'Average Time Per Quiz')
    fig.figure.suptitle('Final Score vs Average Time Per Quiz')
    fig.figure.tight_layout()

    plt.show()


if __name__ == '__main__':
    quiz_path = os.path.join(os.getcwd(), 'quizzes')
    course_performance_with_first_attempt_analysis('grade_book.csv', quiz_path)
