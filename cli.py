import click
import json
from pathlib import Path

from app.models import *
from app import app

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

def handle_collection_config(collection_config):
    with app.app_context():
        collection = Collection(
            name=collection_config['Name']
        )
        db.session.add(collection)
        db.session.add(collection)
        for t in collection_config['Tasks']:
            if t['Type'] == "SequenceClassification":
                # 1. Create Active Learning Stuff
                alc = t['ActiveLearning']
                al_config = ActiveLearningConfigForSequenceClassification(
                    start=alc['Start'],
                    model_name=alc['ModelName'],
                )
                db.session.add(al_config)
                db.session.commit()
                # 2. Create Task Config
                seq_task = SequenceClassificationTask(
                    al_config=al_config.id,
                    collection=collection.id,
                    name=t['Name'],
                    description=t['Description']
                )
                db.session.add(seq_task)
                db.session.commit()
                # Map classes to class config
                for class_label in t['Classes']:
                    task2class = SeqClassificationTaskToClasses(
                        seq_class_task=seq_task.id,
                        class_label=class_label
                    )
                    db.session.add(task2class)
                db.session.commit()


        db.session.add(collection)
        db.session.commit()
        return collection.id


def create_texts_from_list(collection_data, collection_id):
    with app.app_context():
        texts = []
        for idx, t in enumerate(collection_data):
            text = Text(
                collection=collection_id,
                index=idx,
                content=t,
            )
            db.session.add(text)
            texts.append(texts)
        db.session.commit()
        return texts


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
@click.argument('filename', type=click.Path(exists=True))
def from_json(filename):
    with open(filename) as collection_src_f:
        collection_src = json.load(collection_src_f)
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

    collection_id = handle_collection_config(collection_config)

    if isinstance(collection_data, list):
        texts = create_texts_from_list(collection_data, collection_id)
        pass
    else:
        texts = []
        click.echo("Not implemented now.")

    click.echo(f"Imported collection {collection_config['Name']} with {len(texts)} into the application.")


@click.group()
def write_collection():
    pass


@write_collection.command()
@click.option('-name')
@click.option('--only-annotated-texts', is_flag=True)
@click.argument('filename', type=click.Path(exists=False))
def to_json(name, filename, only_annotated_texts):
    with app.app_context():
        collection_query = list(Collection.query.filter_by(name=name))
        if not collection_query:
            click.echo(f"No collection with name {name} in database")
            return
        collection = collection_query[0]
        with open(filename, 'w') as f:
            data = collection.serialize_dict()
            if only_annotated_texts:
                texts = [entry for entry in data['Texts'] if entry['Annotations']]
                data['Texts'] = texts
            json.dump(data, f, indent=4)
        click.echo(f'Created output file {filename}')


cli = click.CommandCollection(sources=[db_handling, create_collection, write_collection])
if __name__ == '__main__':
    cli()
