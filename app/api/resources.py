"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restx import Resource
from flask_restx import reqparse



from .security import require_auth
from . import api_rest
from ..schemes import *
from ..models import *

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

@api_rest.route('/collection/<int:collection_id>/text-index/<int:text_index>')
class TextFromProjectByIndex(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()

    def get(self, collection_id, text_index):
        text = list(Text.query.filter_by(collection=collection_id))[text_index]
        return self.text_schema.dump(text)


@api_rest.route("/collection/<int:collection_id>/text/<int:text_id>/annotation")
class AnnotationEndpoint(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, project_id, text_id):
        pass


    def post(self, collection_id, text_id):
        data = request.json
        text_id = int(data['Text'])
        collection_id = int(data['Collection'])
        class_label = data['Class']
        task_id = int(data['Task'])

        task = SequenceClassificationTask.query.get(task_id)
        possible_classes = SeqClassificationTaskToClasses.query.filter_by(seq_class_task=task.id)
        possible_classes = [c.class_labels for c in possible_classes]
        if class_label not in possible_classes:
            return 
        collection_




        return request.json





