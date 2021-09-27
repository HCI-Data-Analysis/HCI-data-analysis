import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def course_performance_analysis(gradebook_path):
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

    print("25% quantile: " + str(quantile_25percent), " Median: " + str(median),
          " 75% quantile: " + str(quantile_75percent), " Mean: " + str(mean))

    sns.displot(file['Final Score'], kde=True, bins=30, height=5, aspect=1.5)

    plt.axvline(x=w_2015, label='2015: 80.99%', color='r')
    plt.axvline(x=w_2016, label='2016: 79.93%', color='g')
    plt.axvline(x=w_2017, label='2017: 78.70%', color='b')
    plt.axvline(x=w_2018, label='2018: 85.97%', color='c')
    plt.axvline(x=w_2019, label='2019: 83.81%', color='m')
    plt.axvline(x=w_2020, label='2020: 90.80%', color='k')
    plt.axvline(x=mean, label=f'2020 Bowen: {format(mean, ".2f")}%', color='y')
    plt.legend()

    plt.title('Course performance')
    plt.xlabel('Grade')
    plt.ylabel('Number of students')
    plt.xticks(ticks=range(40, 100, 5), labels=range(40, 100, 5))
    plt.yticks(ticks=range(0, 25, 3), labels=range(0, 25, 3))
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    course_performance_analysis('grade_book.csv')
