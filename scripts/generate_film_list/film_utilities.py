import json
from pathlib import Path

def tuples(data_file_path):
    return json.loads(Path(data_file_path).read_text())['films']

def fulltext_title(film, data_file_path='./list.json'):
    return tuples(data_file_path)[film]

def all_titles(data_file_path='./list.json'):
    return iter(tuples(data_file_path).values())
