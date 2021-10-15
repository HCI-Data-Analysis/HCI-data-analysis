import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import os


def course_performance_analysis(gradebook_path):
    file = pd.read_csv(gradebook_path)
    col = 'Overall Final Score'

    mean = file[col].mean()
    standard_dev = file[col].std()
    quantile_25percent = file[col].quantile(.25)
    median = file[col].median()
    quantile_75percent = file[col].quantile(.75)

    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_retrieve_avg, w_2020_retrieve_std = 90.80, 10.5
    w_2020_calculated_avg, w_2020_calculated_std = mean, standard_dev

    winter_averages = [w_2016_avg, w_2017_avg, w_2018_avg, w_2019_avg, w_2020_retrieve_avg, w_2020_calculated_avg]
    winter_deviations = [w_2016_std, w_2017_std, w_2018_std, w_2019_std, w_2020_retrieve_std, w_2020_calculated_std]
    winter_labels = ['W2016', 'W2017', 'W2018', 'W2019', 'W2020', 'H W2020']

    print("25% quantile: " + str(quantile_25percent), " Median: " + str(median),
          " 75% quantile: " + str(quantile_75percent), " Mean: " + str(mean),
          " Standard Deviation: " + str(standard_dev))

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.barh(winter_labels, winter_averages, xerr=winter_deviations, capsize=3)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_xlim([40, 110])
    ax1.set_title('Course Grade History')
    fig.tight_layout()

    ax2.errorbar(winter_labels, winter_averages, yerr=winter_deviations, capsize=4)
    ax2.set_yticks(range(60, 105, 5))

    fig, (ax1) = plt.subplots(1)
    sns.histplot(file[col], kde=True, ax=ax1, bins=30, line_kws={"linewidth": 1}).set(title='Course performance',
                                                                                      xlabel='Grade',
                                                                                      ylabel='Number of students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    fig.tight_layout()
    plt.show()
    
    
def course_performance_with_first_attempt_analysis(GRADEBOOK_PATH, QUIZSCOREJSON_PATH):
    file = pd.read_csv(GRADEBOOK_PATH)
    DATA448ID = file['ID']
    score = file['Overall Final Score']
    pre_test = file['Overall Pre-Tests (880658)']
    post_test = file['Overall Post-Tests (880660)']
  
    first_attempt = {}
    # Key: DATA448ID, Value(array): test score, quiz points possible
    counter = 0
    first_attempt_score = []
    
    # Get first attempt only quiz mark out of JSON files
    for i in os.listdir(QUIZSCOREJSON_PATH): 
        if i.endswith('.json'):
            full_path = os.path.join(QUIZSCOREJSON_PATH, i)
            with open(full_path, 'r') as f:
                file = f.read()
                json_file = json.loads(file)
                for json_block in json_file:
                    if(json_block['attempt'] == 1):
                        if(json_block['user_id'] not in first_attempt):
                            first_attempt[json_block['user_id']] = [[json_block['kept_score'], json_block['quiz_points_possible']]]
                        else:
                            first_attempt_value = first_attempt[json_block['user_id']]
                            first_attempt_value.append([json_block['kept_score'], json_block['quiz_points_possible']])
                            first_attempt[json_block['user_id']] = first_attempt_value
                            
    #print(first_attempt[9620106][0])
    
    # Change current quiz score from overall score and replace it with first attempt only score
    for id in DATA448ID: 
        overall_first_attempt = 0
        test_score = 0
        possible_score = 0
        
        for mark in first_attempt[id]:
            test_score += mark[0]
            possible_score += mark[1]
            
        overall_first_attempt = test_score / possible_score
        overall_without_quiz_score = score[counter] - ((pre_test[counter] + post_test[counter]) / possible_score)
        first_attempt_score.append(overall_without_quiz_score + overall_first_attempt)
        
        counter+=1
        
    #print(score[0], first_attempt_score[0])
    
    first_attempt_score = pd.Series(first_attempt_score)
    
    # Actual Score mean and std
    current_mean = score.mean() #
    current_standard_dev = score.std()
    
    # First attempt only score mean and std
    mean = first_attempt_score.mean()
    standard_dev = first_attempt_score.std()
    quantile_25percent = first_attempt_score.quantile(.25)
    median = first_attempt_score.median()
    quantile_75percent = first_attempt_score.quantile(.75)
    
    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_retrieve_avg, w_2020_retrieve_std = 90.80, 10.5
    w_2020_calculated_avg, w_2020_calculated_std = current_mean, current_standard_dev
    w_2020_first_attempt_avg, w_2020_first_attempt_std = mean, standard_dev

    winter_averages = [w_2016_avg, w_2017_avg, w_2018_avg, w_2019_avg, w_2020_retrieve_avg, w_2020_calculated_avg, w_2020_first_attempt_avg]
    winter_deviations = [w_2016_std, w_2017_std, w_2018_std, w_2019_std, w_2020_retrieve_std, w_2020_calculated_std, w_2020_first_attempt_std]
    winter_labels = ['W2016', 'W2017', 'W2018', 'W2019', 'W2020', 'H W2020', 'F 2020']

    print("25% quantile: " + str(quantile_25percent), " Median: " + str(median),
          " 75% quantile: " + str(quantile_75percent), " Mean: " + str(mean),
          " Standard Deviation: " + str(standard_dev))

    # 1) Mean and Standard Deviation graph
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.barh(winter_labels, winter_averages, xerr=winter_deviations, capsize=3)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_xlim([40, 110])
    ax1.set_title('Course Grade History')
    fig.tight_layout()

    ax2.errorbar(winter_labels, winter_averages, yerr=winter_deviations, capsize=4)
    ax2.set_yticks(range(60, 105, 5))

    # 2) Density plot graph for First attempt only score
    fig, (ax1) = plt.subplots(1)
    sns.histplot(first_attempt_score, kde=True, ax=ax1, bins=30, line_kws={"linewidth": 1}).set(title='Course performance',
                                                                                      xlabel='Grade',
                                                                                      ylabel='Number of students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    fig.tight_layout()
    
    # 3) Histgram comparsion plot for Actual score and First attempt only score
    fig, (ax1) = plt.subplots(1)
    for a in [score, first_attempt_score]:
        sns.histplot(a, kde=False, ax = ax1, bins=30, line_kws={"linewidth": 1}).set(title='Course performance comparsion',
                                                                                        xlabel='Grade',
                                                                                        ylabel='Number of students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    
    
    plt.show()
    

if __name__ == '__main__':
    #course_performance_analysis('grade_book.csv')
    quiz_path = os.path.join(os.getcwd(), 'quizzes')
    course_performance_with_first_attempt_analysis('grade_book.csv', quiz_path)
