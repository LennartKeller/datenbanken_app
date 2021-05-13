"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restx import Resource

from . import api_rest
from .security import require_auth
from ..schemes import *


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp, 'id': resource_id}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}


@api_rest.route('/test/<string:id>')
class TestResource(Resource):

    def get(self, id):
        timestamp = datetime.utcnow().isoformat()
        return {
            'hello': 'world',
            'timestamp': timestamp,
            'id': id
        }


@api_rest.route('/text')
class AllTexts(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema(many=True)

    def get(self):
        all_texts = Text.query.all()
        return self.text_schema.dump(all_texts)


@api_rest.route('/text/<int:id>')
class SingleText(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()

    def get(self, id):
        text = Text.query.get(id)
        return self.text_schema.dump(text)


@api_rest.route('/collection')
class AllCollectionsResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_schema = CollectionSchema(many=True)

    def get(self):
        collections = Collection.query.all()
        return self.collection_schema.dump(collections)


@api_rest.route('/collection/<int:collection_id>/text-index/<int:text_index>')
class TextFromProjectByIndex(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()

    def get(self, collection_id, text_index):
        text = list(Text.query.filter_by(collection=collection_id))[text_index]
        return self.text_schema.dump(text)


@api_rest.route("/text/seqclass/<int:text_id>/task/<int:task_id>/annotation")
class SingleAnnotationEndpoint(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, text_id, task_id):
        annotation = list(SequenceClassificationAnnotation.query.filter_by(text=text_id, seq_task=task_id))
        if not annotation:
            return None, 200

    def post(self, text_id, task_id):
        data = request.json
        class_label = data['Class']
        task_id_body = int(data['Task'])
        if task_id_body != task_id:
            return {'error': 'Task id from URL and body do not match'}, 500

        task = SequenceClassificationTask.query.get(task_id)
        possible_classes = SeqClassificationTaskToClasses.query.filter_by(seq_class_task=task.id)
        possible_classes = [c.class_label for c in possible_classes]
        if class_label not in possible_classes:
            return {'error': 'Invalid class label'}, 500

        existing_annotation = list(SequenceClassificationAnnotation.query.filter_by(text=text_id, seq_task=task_id))
        if existing_annotation:
            db.session.delete(existing_annotation[0])
            db.session.commit()

        class_label_obj = list(SeqClassificationTaskToClasses.query.filter_by(class_label=class_label))[0]
        annotation = SequenceClassificationAnnotation(
            text=text_id,
            seq_task=task_id,
            class_label=class_label_obj.id
        )
        try:
            db.session.add(annotation)
            db.session.commit()
            return {'success': True}, 200
        except Exception as e:
            return {"error": e}, 500
