from statistics import mean

from sklearn.cluster import KMeans


def average_kmeans_iterations(survey_df, n_iter):
    """
    This function determines the average iterations for kmeans.
    :param survey_df: the processed data to run kmeans on.
    :param n_iter: the number of iterations to run kmeans for.
    """
    cluster_data = survey_df.iloc[:, 1:6]
    iterations = []
    for _ in range(n_iter):
        model = KMeans(n_clusters=3, n_init=500).fit(cluster_data)
        iterations.append(model.n_iter_)
    print('Average k-means iterations: ', round(mean(iterations)))
