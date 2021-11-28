import jinja2
import json
from pathlib import Path

films = json.loads(Path('./list.json').read_text())

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))
template = env.get_template('films.html')

html = template.render(films=films['films'].keys())
Path('./generated').mkdir(exist_ok=True)
Path('./generated/films.html').write_text(html)
