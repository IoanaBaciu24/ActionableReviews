"""Main module for the clustering app"""
import argparse
import numpy as np
import pandas as pd
from config import get_json_from_config
from app_clustering.embed_reviews import embed_dataset, embedding_string_to_list
from app_clustering.clustering import run_kmeans, plot_results, get_labels_via_kmeans


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the config file')
    config_path = parser.parse_args().config
    config = get_json_from_config(config_path)
    # embed the reviews
    if config["embed"] == "True":
        dataset = pd.read_csv(config["source_path"])
        dataset = dataset[dataset["class"]]
        embed_dataset(dataset,config["embedding_model"], config["embeddings_path"])
    dataset_embeddings = pd.read_csv(config["embeddings_path"])
    # apply elbow method to get a good number of clusters
    if config["elbow"] == "True":
        min_clusters = int(config["min_clusters"])
        max_clusters = int(config["max_clusters"])
        dataset_embeddings["embedding_list"] = dataset_embeddings["embedding"].apply(lambda x: embedding_string_to_list(x))
        embeddings = np.array(dataset_embeddings["embedding_list"].to_list())
        k_sizes, intertias = run_kmeans(embeddings, min_clusters, max_clusters)
        if config["do_plot"] == "True":
            plot_results(k_sizes, intertias)
    # run kmeans and label dataset
    if config["label_reviews"] == "True":
        k = config["number_of_clusters"]
        dataset_embeddings["embedding_list"] = dataset_embeddings["embedding"].apply(lambda x: embedding_string_to_list(x))
        embeddings = np.array(dataset_embeddings["embedding_list"].to_list())
        dataset_embeddings["label"] = get_labels_via_kmeans(embeddings, k)
        dataset_embeddings.to_csv(config["output_labels_path"], index=False)
