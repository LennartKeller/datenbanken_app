def collection_to_dict(collection, only_annotated_texts=False):
    data = collection.serialize_dict()
    if only_annotated_texts:
        texts = [entry for entry in data['Texts'] if entry['Annotations']]
        data['Texts'] = texts
    return data