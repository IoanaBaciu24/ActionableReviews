import json

def get_json_from_config(path: str):
    """Function that returns the config_dict"""
    f = open(path)
    text = f.read()
    return json.loads(text)