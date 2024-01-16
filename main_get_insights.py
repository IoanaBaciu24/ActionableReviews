import argparse
from config import get_json_from_config
from app_get_inisghts.get_insights import InsightsHandler
from app_get_inisghts.llm import LLM


def init_llm(config: dict):
    
    template_path = config["prompt_template_path"]
    with open(template_path, "r") as f:
        prompt_template = f.read()
    model = config["model"]
    temperature = config["temperature"]
    return LLM(prompt_template, model, temperature)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the config file')
    config_path = parser.parse_args().config
    config_json = get_json_from_config(config_path)
    llm = init_llm(config_json)
    insights_handler = InsightsHandler(llm, config_json)
    insights_handler.run_insights()
