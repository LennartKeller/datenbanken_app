"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restx import Resource

from . import api_rest
from .security import require_auth
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

@api_rest.route('/text/<int:text_id>/discard')
class DiscardText(Resource):
    def get(self, text_id):
        text = Text.query.get(text_id)
        text.discarded = True
        db.session.add(text)
        db.session.commit()
        return {'success': True}, 200

@api_rest.route('/collection')
class AllCollectionsResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection_schema = CollectionSchema(many=True)

    def get(self):
        collections = Collection.query.all()
        return self.collection_schema.dump(collections)


# TODO Remove ASAP
@api_rest.route('/collection/<int:collection_id>/text-index/<int:text_index>')
class TextFromProjectByIndex(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_schema = TextSchema()

    def get(self, collection_id, text_index):
        text = list(Text.query.filter_by(collection=collection_id))[text_index]
        return self.text_schema.dump(text)


@api_rest.route("/text/<int:text_id>/seq-class-task/<int:task_id>/annotation")
class SingleAnnotationEndpoint(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seq_class_to_class_schema = SequenceClassificationTaskSchema()

    def get(self, text_id, task_id):
        annotation = list(SequenceClassificationAnnotation.query.filter_by(text=text_id, seq_task=task_id))
        if not annotation:
            return None, 200
        annotation = annotation[0]
        class_label_entry = SeqClassificationTaskToClasses.query.get(annotation.class_label)
        return self.seq_class_to_class_schema.dump(class_label_entry)

    def post(self, text_id, task_id):
        data = request.json
        class_label = data['class']

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


@api_rest.route('/collection/<int:collection_id>/tasks')
class TasksOfCollectionResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seq_task_schema = SequenceClassificationTaskSchema(many=True)

    def get(self, collection_id):
        tasks_dumps = []
        # Get sequence classification tasks
        seq_class_tasks = SequenceClassificationTask.query.filter_by(collection=collection_id)
        seq_class_tasks_dumps = self.seq_task_schema.dump(seq_class_tasks)
        for t in seq_class_tasks_dumps:
            t['type'] = "SequenceClassification"
            tasks_dumps.append(t)
        return tasks_dumps


@api_rest.route('/sequence-classification/<int:task_id>')
class SequenceClassificationConfigurationResource(Resource):

    def get(self, task_id):
        # get classes
        classes = [
            c.class_label for c in SeqClassificationTaskToClasses.query.filter_by(seq_class_task=task_id)
        ]
        return {'classLabels': classes}

@api_rest.route('collection/<int:collection_id>/next')
class NextTextResource(Resource):

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.queue = []
        self.text_schema = TextSchema()
        self.al_components = {}

    def get(self, collection_id):

        # 1. Option : If there is any text left in queue just return it ..
        if self.queue:
            text = self.queue.pop()

        # 2. Option: Active Learning
        # 2.1 Suboption: Active Learning is registered but not yet enabled
        # => Enable it (If each label from config is in the data at least once)
        # 2.X: Finally draw an instance for each al task return first put other in queue
        if self.al_components:
            pass


        # 3. Option: If there os no active learning registered or active just return texts sorted by index
        if not self.al_components:
            pass



        return self.text_schema.dump(text)

