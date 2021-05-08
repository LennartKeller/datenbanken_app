import click
import json
from pathlib import Path

from app.models import db, Corpus, Text
from app.schemes import CorpusSchema, TextSchema
from app import app

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.group()
def db_handling():
    pass

@db_handling.command()
def init_db():
    with app.app_context():
        db.create_all()

@db_handling.command()
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
def drop_db():
    with app.app_context():
        db.drop_all()


@click.group()
def read_corpus():
    pass

@read_corpus.command()
@click.option('-n', '--name')
@click.option('-s', '--seperator', default="\n", show_default=True)
@click.argument('filename', type=click.Path(exists=True))
def read_plain_text(name, seperator, filename):
    corpus_data = Path(filename).read_text()
    texts = corpus_data.split(seperator)

    with app.app_context():
        corpus = Corpus(name=name)
        db.session.add(corpus)
        db.session.commit()

        for idx, t in enumerate(texts):
            text = Text(text=t, corpus=corpus.id, index=idx)
            db.session.add(text)
        db.session.commit()
    click.echo(f"Loaded Corpus {name} with {len(texts)} texts into the application!")


@click.group()
def read_project():
    pass

@read_project.command()
@click.argument('filename', type=click.Path(exists=True))
def init_project(filename):
    with open(filename) as config_file:
        config = json.load(config_file)
    project_name = config['Name']
    corpora = config['Corpora']
    sequence_annotation_config = config['SequenceAnnotation']
    active_learning_config = config['ActiveLearningConfig']



cli = click.CommandCollection(sources=[db_handling, read_corpus, read_project])
if __name__ == '__main__':
    cli()
