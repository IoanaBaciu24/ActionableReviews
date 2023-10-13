import json

def get_json_from_config(path: str):
    """Function that returns the config_dict"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
        return json.loads(text)
