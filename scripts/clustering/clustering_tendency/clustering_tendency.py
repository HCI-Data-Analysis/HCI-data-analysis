import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from pyclustertend import vat, ivat, hopkins


def average_hopkins_statistic(data: np.ndarray, num_runs=500):
    hopkins_scores = []
    for i in range(0, num_runs):
        H = 1 - hopkins(data, 40)
        hopkins_scores.append(H)

    return sum(hopkins_scores) / len(hopkins_scores)


def clustering_tendency(survey_df: DataFrame):
    survey_array = survey_df.values

    average_H = average_hopkins_statistic(survey_array, 500)

    # Plot visual assessment of tendency graphs. This wouldn't show when run in terminal, so Google Colab was used.
    ordered_matrix_i = ivat(survey_array, return_odm=True)
    figure_size = (10, 10)
    _, ax = plt.subplots(figsize=figure_size)
    ax.imshow(ordered_matrix_i, cmap='pink', vmin=0, vmax=np.max(ordered_matrix_i))

    ordered_matrix = vat(survey_array, return_odm=True)
    figure_size = (10, 10)
    _, ax = plt.subplots(figsize=figure_size)
    ax.imshow(ordered_matrix, cmap='pink', vmin=0, vmax=np.max(ordered_matrix))

    print(f'Hopkins statistics: {average_H}')
