from flask import Flask, abort, render_template, request
import json
from pathlib import Path

app = Flask(__name__)

def dummy_response():
    return json.loads(Path('testdata/search_response2.json').read_text())

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method != 'POST':
        main()

    return render_template('results.html', movies=dummy_response()['Search'])
