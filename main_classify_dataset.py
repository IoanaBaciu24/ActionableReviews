"""Main module for classifier app"""
import argparse
import pandas as pd
from config import get_json_from_config
from app_actionable_classification.classifier import ActionableReviewClassifierChat, \
    ActionableReviewClassifierInstructLLM, ActionableReviewClassifier

def run_classification(dataset: pd.DataFrame,
                       classifier: ActionableReviewClassifier, output_path: str):
    """Save to file classes for the reviews"""
    dataset["class"] = dataset["content"].apply(lambda x: classifier(x))
    dataset.to_csv(output_path, index=False)

def classify_dataset(config: dict):
    """Wrapper function for the classification step"""
    dataset = pd.read_csv(config["dataset_path"])
    if config["type"] == "chat":
        classifier = ActionableReviewClassifierChat(model=config["model"])
    else:
        classifier = ActionableReviewClassifierInstructLLM(model=config["model"])
    run_classification(dataset, classifier, config["output_path"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the config file')
    config_path = parser.parse_args().config
    config = get_json_from_config(config_path)
    classify_dataset(config)
