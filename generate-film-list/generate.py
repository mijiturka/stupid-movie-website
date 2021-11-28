import jinja2
from pathlib import Path

films = Path('./list.md').read_text().splitlines()

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
template = env.get_template('film-list.html')

html = template.render(films=films)
print(html)
