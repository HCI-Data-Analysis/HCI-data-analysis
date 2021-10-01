import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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


if __name__ == '__main__':
    course_performance_analysis('grade_book.csv')
