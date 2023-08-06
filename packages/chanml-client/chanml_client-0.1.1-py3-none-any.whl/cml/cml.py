import typer
import requests
import random
from datetime import datetime
from tqdm import tqdm
import json
import os
from pygments import highlight, lexers, formatters


app = typer.Typer()

BASE_URL = 'https://beta.chanml.com/api/v1/'
ACCESS_KEY = os.environ.get('CHANML_API_TOKEN', '')
headers = {'Authorization' :'Token '+ACCESS_KEY}

@app.command()
def new_experiment(name:str="default project", project_id:int=0, url:str=BASE_URL+"experiments/"):
    data = {
        "name": name,
        "project": project_id
    }

    b = requests.post(url, headers=headers, json=data)
    formatted_json = json.dumps(b.json(), indent=4, sort_keys=True)
    colorful_json = highlight(formatted_json,  lexers.JsonLexer(), formatters.TerminalFormatter())
    typer.echo(colorful_json)


def test(
        a: float=random.uniform(1.1,5.4) , 
        b: float=random.uniform(1.1,5.4) , 
        experiment: int=7, 
        url:str="",
        owner:int=4,
        time=str(datetime.now()),
    ):
    data = {
        'experiment': experiment,
        'owner': owner,
        'time': time,
        'data': {
            'batch_regularization_loss': a,
            'categorical_accuracy': b,
        }
    }

    b = requests.post(url, headers=headers, json=data)
    # typer.echo(b.text)

@app.command()
def list_project():
    url = BASE_URL+"projects/"
    a = requests.get(url, headers=headers).json()
    names = [{i.get('id',''): i.get("name", '')} for i in a.get('results', [])]

    formatted_json = json.dumps(names, indent=4, sort_keys=True, ensure_ascii=False)
    colorful_json = highlight(formatted_json,  lexers.JsonLexer(), formatters.TerminalFormatter())
    typer.echo(colorful_json)


@app.command()
def list_experiment():
    url = BASE_URL+"experiments/"
    a = requests.get(url, headers=headers).json()
    names = [{i.get('id',''): i.get("name", '')} for i in a.get('results', [])]

    formatted_json = json.dumps(names, indent=4, sort_keys=True, ensure_ascii=False)
    colorful_json = highlight(formatted_json,  lexers.JsonLexer(), formatters.TerminalFormatter())
    typer.echo(colorful_json)


@app.command()
def version():
    typer.echo("0.1.1")

@app.command()
def log_metric(
        r:int = 10, 
        eid:int=8, 
        url:str=BASE_URL+"metrics/",
    ):
    for i in tqdm(range(r)):
        test(
            a=random.uniform(0.5, 3.0), 
            b=random.uniform(0.3, 4.0), 
            experiment=eid,
            url = url)

if __name__ == "__main__":
    app()