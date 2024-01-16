import pandas as pd
from app_get_inisghts.llm import LLM

class InsightsHandler:
    def __init__(self, llm: LLM, config_dict: dict) -> None:
        self.llm = llm
        self.config = config_dict

    def get_insights_per_topic(self, df_labeled: pd.DataFrame, topic_number: int):
        reviews_per_topic = df_labeled[df_labeled["label"] == topic_number]["content"].to_list()
        result = {"topic": topic_number, "response":self.llm(reviews_per_topic)}
        return result

    def run_insights(self):
        labeled_dataframe = pd.read_csv(self.config["input_dataframe_path"])
        label_count = self.config["label_count"]
        list_of_dicts = []
        for label in range(label_count):
            d = self.get_insights_per_topic(labeled_dataframe, label)
            list_of_dicts.append(d)
        default_value_for_missing = None
        df_results = pd.DataFrame(list_of_dicts)
        df_results.to_csv(self.config["output_path"])        
