import jinja2
from pathlib import Path

films = Path('./list.md').read_text().splitlines()

html = jinja2.Template("{% for film in films -%} FILM: {{film}} \n{% endfor %}").render(films=films)
print(html)
