"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restx import Resource

from .security import require_auth
from . import api_rest
from ..schemes import TextSchema
from ..models import Text

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
class AllTexts(Resource):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()
    
    def get(self, id):
        text = Text.query.get(id)
        return self.text_schema.dump(text)