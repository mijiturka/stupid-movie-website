import json
from pathlib import Path

def tuples():
    return json.loads(Path('./list.json').read_text())['films']

def fulltext_title(film):
    return tuples()[film]

def all_titles():
    return iter(tuples().values())
