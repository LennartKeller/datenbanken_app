import click
import json
from pathlib import Path

from app.models import *
from app.tools import collection_to_dict, handle_collection_config, create_texts_from_list, create_texts_from_read_config
from app import app, db

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.group()
def db_handling():
    pass


@db_handling.command()
def init_db():
    db_path = Path('./app/db')
    if not db_path.exists():
        db_path.mkdir()

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
def create_collection():
    pass

@create_collection.command()
@click.argument('filename', type=click.File('r'))
def from_json(filename):

    collection_src = json.load(filename)
    try:
        collection_config = collection_src['Config']
    except KeyError:
        click.echo("Invalid collection src. Missing config section!")
        return

    try:
        collection_data = collection_src['Texts']
    except KeyError:
        click.echo("Invalid collection src. Missing data section!")
        return
    with app.app_context():
        collection_id = handle_collection_config(collection_config)

    if isinstance(collection_data, list):
        with app.app_context():
            texts = create_texts_from_list(collection_data, collection_id)
    elif isinstance(collection_data, dict):
        with app.app_context():
            try:
                texts = create_texts_from_read_config(collection_data, collection_id)
            except Exception as e:
                click.echo(e)
                return

    # Finally commit all changes to the db
    with app.app_context():
        db.session.commit()
    click.echo(f"Imported collection {collection_config['Name']} with {len(texts)} into the application.")


@click.group()
def write_collection():
    pass


@write_collection.command()
@click.option('--name', '-n', required=True)
@click.option('--only-annotated-texts', is_flag=True)
@click.argument('filename', type=click.File('w'))
def to_json(name, filename, only_annotated_texts):
    with app.app_context():
        collection_query = list(Collection.query.filter_by(name=name))
        if not collection_query:
            click.echo(f"No collection with name {name} in database")
            return
        collection = collection_query[0]
        data = collection_to_dict(collection, only_annotated_texts=only_annotated_texts)
        json.dump(data, filename)
        click.echo(f'Created output file {filename.name}')


cli = click.CommandCollection(sources=[db_handling, create_collection, write_collection])
if __name__ == '__main__':
    cli()
