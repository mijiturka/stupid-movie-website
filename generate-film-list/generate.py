import jinja2
from pathlib import Path

films = Path('./list.md').read_text().splitlines()

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
template = env.get_template('films.html')

html = template.render(films=films)
Path('./generated').mkdir(exist_ok=True)
Path('./generated/films.html').write_text(html)
