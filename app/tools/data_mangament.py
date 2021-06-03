from typing import Dict

from ..models import \
    Collection, \
    db, \
    SeqClassificationTaskToClasses, \
    SequenceClassificationTask, \
    ActiveLearningConfigForSequenceClassification, \
    Text


def collection_to_dict(collection, only_annotated_texts=False):
    """
    Returns the data of the passed collection db-object as dictionary.
    Args:
        collection: Collection to serialize as dict
        only_annotated_texts: Whether or not not annotated texts should be included in the output

    Returns:
        Dictionary with same structure as the collection config json file from which it was created.

    """
    data = collection.serialize_dict()
    if only_annotated_texts:
        texts = [entry for entry in data['Texts'] if entry['Annotations']]
        data['Texts'] = texts
    return data


def handle_collection_config(collection_config: Dict):
    """
    Creates a collection and all its config dependencies from the passed dictionary.
    Args:
        collection_config: Dictionary with all the config parts.
        Has to be of the same structure as a config json file

    Returns:
        The id of the newly created collection config the database.
    """
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
    """
    Inserts text from a collection configuration into the db.

    Args:
        collection_data: Lists of texts to insert
        collection_id: db-Id of the collection configuration

    Returns:
        List of Texts db-objects
    """
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

def create_texts_from_read_config(read_config):
    pass