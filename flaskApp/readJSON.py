import json


def read_json(file):
    f = open(file)
    return json.load(f)
