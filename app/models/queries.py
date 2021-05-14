from .data_model import *


def get_unannotated_texts(collection_id: int):
    all_texts = set(Text.query.filter_by(discarded=False, collection=collection_id))
    annotated_texts = set(
        Text.query.join(SequenceClassificationAnnotation, Text.id == SequenceClassificationAnnotation.text)
    )
    unannotated_texts = all_texts - annotated_texts
    return list(sorted(unannotated_texts, key=lambda t: t.index))

def get_tasks(colletion_id: int):
    pass
