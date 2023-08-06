import os, json

def get_files(folder, contains = 'INMET_SE_ES_'):
    folder = './{folder}'.format(folder = folder)
    return list(filter(lambda k: str(contains) in k, os.listdir(folder)))

def open_json(json_file):
    with open(json_file) as data:
        return json.load(data)