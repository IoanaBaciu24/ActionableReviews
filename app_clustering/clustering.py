"""Module that contains functions related to the clustering step"""
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def run_kmeans(dataset: np.array, min_clusters: int, max_clusters: int) -> [List[int], List[float]]:
    """Function that runs kmeans for a range of clusters, and returns intertias.
       It creates the data we will use for the elbow method."""
    number_of_clusters = list(range(min_clusters, max_clusters+1))
    inertias = []
    for k in number_of_clusters:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(dataset)  
        inertias.append(kmeans.inertia_)
    return number_of_clusters, inertias


def plot_results(number_of_clusters:List[int], inertias: List[float]):
    """Elbow method plot"""
    plt.plot(number_of_clusters, inertias, marker='o')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.show()


def get_labels_via_kmeans(dataset: np.array, k: int):
    """Function that gets the cluster for the input dataset"""
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(dataset)
    return kmeans.labels_
