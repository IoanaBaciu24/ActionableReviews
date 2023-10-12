"""Module to test the quality of ActionableReviewClassifier"""
import argparse
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from config import get_json_from_config
from app_actionable_classification.classifier import ActionableReviewClassifierChat, \
        ActionableReviewClassifierInstructLLM, ActionableReviewClassifier

def run_classifier(dataset: pd.DataFrame, clf: ActionableReviewClassifier):
    """Function that runs the classifier on the dataset, returns classification reoprt"""
    reviews = dataset["content"]
    predictions = []
    for review in reviews:
        predictions.append(clf(review))
    return classification_report(dataset["actionable"], predictions, output_dict=True), \
            confusion_matrix(dataset["actionable"], predictions)

def main(config: dict):
    dataset = pd.read_csv(config["dataset_path"])
    if config["type"] == "chat":
        clf = ActionableReviewClassifierChat(model=config["model"])
    else:
        clf = ActionableReviewClassifierInstructLLM(model=config["model"])
    report, matrix = run_classifier(dataset, clf)
    print(report)
    print(matrix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the dataset')
    config = get_json_from_config(parser.parse_args().config)
    main(config)
