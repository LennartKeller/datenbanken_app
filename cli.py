import click
import json
from pathlib import Path

from app.models import *
from app import app

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
    sequence_annotation_config = config['SequenceAnnotationConfig']
    active_learning_config = config['ActiveLearningConfig']
    # TODO Validation
    # 1. Validate corpus refs
    #
    # Create Annotation Config
    categories = sequence_annotation_config.get("Categories", [])
    labels = sequence_annotation_config.get("Labels", [])

    with app.app_context():
        sequence_annotation_config = SequenceAnnotationConfig()
        db.session.add(sequence_annotation_config)
        db.session.commit()

        for category in categories:
            category = Category(
                sequence_annotation_config=sequence_annotation_config.id,
                value=category
            )
            db.session.add(category)
            db.session.commit()

            seqconf_to_cat = SequenceAnnotationConfigToCategory(
                config_id=sequence_annotation_config.id,
                category_id=category.id
            )
            db.session.add(seqconf_to_cat)
            db.session.commit()


        for label in labels:
            label = Label(
                sequence_annotation_config=sequence_annotation_config.id,
                value=label
                )
            db.session.add(label)
            db.session.commit()

            seqconf_to_label = SequenceAnnotationConfigToLabel(
                config_id=sequence_annotation_config.id,
                label_id=category.id
            )
            db.session.add(seqconf_to_label)
            db.session.commit()

        # Create Active Learning Config
        estimator_name = active_learning_config.get("Estimator", {}).get("Name")
        estimator_path = active_learning_config.get("Estimator", {}).get("Path")
        al_task = active_learning_config.get("On", {}).get("Task")
        al_objective = active_learning_config.get("On", {}).get("Objective")


        al_config = ActiveLearningConfig(
            estimator_path=estimator_path,
            estimator_name=estimator_name,
            task=al_task,
            objective=al_objective
        )
        db.session.add(al_config)
        db.session.commit()

        # Create Project
        project = Project(
            name=project_name,
            active_learning_config=al_config.id,
            sequence_annotation_config=sequence_annotation_config.id,
        )

        db.session.add(project)
        db.session.commit()

        # Create Corpus Project Mapping
        c_objs = []
        for c in corpora:
            corpus = list(Corpus.query.filter_by(name=c))
            if not corpus:
                click.echo(f"Warning: Could not find Corpus {c}")
                continue
            corpus = corpus[0]
            c_objs.append(corpus)

        for c in c_objs:
            p2c = ProjectToCorpus(
                project_id=project.id,
                corpus_id=corpus.id
            )
            db.session.add(p2c)
        db.session.commit()


cli = click.CommandCollection(sources=[db_handling, read_corpus, read_project])
if __name__ == '__main__':
    cli()
