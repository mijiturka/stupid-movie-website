import jinja2
import json
from pathlib import Path


def template():
    env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
    return env.get_template('films.html')

def write(html, file_name):
    Path('./generated').mkdir(exist_ok=True)
    Path(f'./generated/{file_name}').write_text(html)

# Get info on all films
films = json.loads(Path('./list.json').read_text())
# Generate a page with the full list of films
html = template().render(films=films['films'].items())
write(html, 'films.html')
