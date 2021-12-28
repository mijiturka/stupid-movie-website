import json
from pathlib import Path

def fulltext_title(film):
    return json.loads(Path('./list.json').read_text())['films'][film]
