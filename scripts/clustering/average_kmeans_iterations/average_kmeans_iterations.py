from statistics import mean

from sklearn.cluster import KMeans


def average_kmeans_iterations(cluster_data, n_iter, k):
    """
    This function determines the average iterations for kmeans.
    :param cluster_data: the processed data to run kmeans on.
    :param n_iter: the number of iterations to run kmeans for.
    :param k: the number of clusters.
    """
    iterations = []
    for _ in range(n_iter):
        model = KMeans(n_clusters=k, n_init=500).fit(cluster_data)
        iterations.append(model.n_iter_)
    print('Average k-means iterations: ', round(mean(iterations)))
