"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restx import Resource


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

@api_rest.route('/project/<int:project_id>/text-index/<int:text_index>')
class TextFromProjectByIndex(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()

    def get(self, project_id, text_index):
        project = Project.query.get(project_id)
        corpora = list(ProjectToCorpus.query.filter_by(project_id=project.id))
        texts = []
        for c in corpora:
            c_texts = Text.query.filter_by(corpus=c.corpus_id)
            texts.extend(c_texts)
        try:
            return self.text_schema.dump(texts[text_index])
        except IndexError as e:
            return {'error': str(e)}, 404

@api_rest.route("/project/<int:project_id>/text/<int:text_id>/annotation")
class AnnotationOfText(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_schema = CategorySchema(many=True)
        self.label_schema = LabelSchema(many=True)

    def get(self, project_id, text_id):
        project = Project.query.get(project_id)
        text = Text.query.get(text_id)

        cat_query = TextToCategory.query.filter_by(text_id=text.id, project_id=project.id)
        label_query = TextToLabel.query.filter_by(text_id=text.id, project_id=project.id)

        labels = [Label.query.get(l.label_id) for l in label_query]
        categories = [Category.query.get(c.category_id) for c in cat_query]

        return self.label_schema.dump(labels), self.cat_schema.dump(categories)
    
    def put(self, project_id, text_id):
        category = request.form.get('category')
        labels = request.form.get('labels')

        project = Project.query.get(project_id)
        text = Text.query.get(text_id)

        

        if category:
            cat = list(Category.query.filter_by(
                value=category,
                sequence_annotation_config=project.sequence_annotation_config
                )
            )
            if not cat:
                return {"error": "invalid category"}, 500
            cat = cat[0]
            new_cat = TextToCategory(text_id=text.id, project_id=project.id, category_id=cat.id)
            db.session.add(new_cat)
            db.session.commit()

        return 200




