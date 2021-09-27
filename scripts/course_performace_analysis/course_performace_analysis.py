import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def course_performace_analysis(gradebook_path):
    file = pd.read_csv(gradebook_path)
    w_2015 = 80.99
    w_2016 = 79.93
    w_2017 = 78.70
    w_2018 = 85.97
    w_2019 = 83.81
    w_2020 = 90.80
    
    mean = file['Final Score'].mean()
    standard_dev = file['Final Score'].std
    quantile_25percent = file['Final Score'].quantile(.25)
    median = file['Final Score'].median()
    quantile_75percent = file['Final Score'].quantile(.75)
    
    print("25% quantile: " + str(quantile_25percent)," Median: " + str(median), " 75% quantile: " + str(quantile_75percent), " Mean: " + str(mean))
    
    sns.displot(file['Final Score'], kde=True, bins = 30)
    
    plt.title('Course performace')
    plt.xlabel('Grade')
    plt.ylabel('amount of student')
    plt.show()
    
    
    
if __name__ == '__main__':
    course_performace_analysis('grade_book.csv')