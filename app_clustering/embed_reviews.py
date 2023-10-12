"""Module with functions related to the embedding of the reviews"""
from tqdm import tqdm
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def embed_dataset(dataset: pd.DataFrame, model_name: str, output_path: str):
    """Function that embeds the reviews and saves the embeddings in a file"""
    model = SentenceTransformer(model_name)
    content_list = dataset["content"].to_list()
    embeddings = []
    for content in tqdm(content_list):
        embeddings.append(model.encode(content, normalize_embeddings=False))
    dataset["embedding"] = embeddings
    dataset['embedding'] = dataset['embedding'].apply(lambda x: ' '.join(map(str, x)))
    dataset.to_csv(output_path, index=False)


def embedding_string_to_list(embedding_str: str) -> list:
    """Converts string embeddings to a list of floats"""
    tokens = embedding_str.split(' ')
    return list(map(float, tokens))
