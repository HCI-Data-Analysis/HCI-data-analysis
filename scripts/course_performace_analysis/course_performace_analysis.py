import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def course_performace_analysis(gradebook_path):
    file = pd.read_csv(gradebook_path)
    # sns.distplot(file['Final Score'], hist=True, kde=True, 
    #          bins=int(180/5), color = 'darkblue', 
    #          hist_kws={'edgecolor':'black'},
    #          kde_kws={'linewidth': 4})
    sns.displot(file['Final Score'], kde=True, bins = 30)
    
    plt.title('Course performace')
    plt.xlabel('Grade')
    plt.ylabel('amount of student')
    plt.show()
    
    
    
if __name__ == '__main__':
    course_performace_analysis('grade_book.csv')