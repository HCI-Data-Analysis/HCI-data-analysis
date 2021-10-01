import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def course_performance_analysis(gradebook_path):
    file = pd.read_csv(gradebook_path)
    col = 'Overall Final Score'
    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_avg, w_2020_std = 90.80, 10.5

    mean = file[col].mean()
    standard_dev = file[col].std()
    quantile_25percent = file[col].quantile(.25)
    median = file[col].median()
    quantile_75percent = file[col].quantile(.75)

    print("25% quantile: " + str(quantile_25percent), " Median: " + str(median),
          " 75% quantile: " + str(quantile_75percent), " Mean: " + str(mean), " Standard Deviation: " + str(standard_dev))
    
    df_year_score = pd.DataFrame({'Average Score': [w_2016_avg,w_2017_avg,w_2018_avg,w_2019_avg,w_2020_avg],'Standard Deviation': [w_2016_std,w_2017_std,w_2018_std,w_2019_std,w_2020_std] },columns=['Average Score','Standard Deviation'])
    df_year_score.index = ['Winter 2016', 'Winter 2017', 'Winter 2018', 'Winter 2019', 'Winter 2020']
    df_year_score.plot(kind = "barh",y = 'Average Score', legend = False,
            title = "COSC 341 Averge Scores Years Compare", xerr = "Standard Deviation")
    
    fig, ax = plt.subplots()
    
    sns.displot(file[col], kde=True, ax=ax, bins=30, height=5, aspect=1.5).set(title='Course performance', xlabel='Grade', ylabel='Number of students')

    ax.set_xticks(range(40, 110, 5))
    ax.set_xticklabels([f'{i}%' for i in range(40, 110, 5)])
    ax.set_yticks(range(0, 25, 3))
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    course_performance_analysis('grade_book.csv')
