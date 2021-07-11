from datetime import datetime

from more_itertools import flatten

from . import db

# This file contains the table definitions for the Database-Relations.
# Some of the models are extend by custom methods to facilitate their use in Python.
# Each frequently model used method has a serialization method
# to convert an entry into a json-compliant dict representation.

class Collection(db.Model):
    __tablename__ = 'Collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f'Corpus {self.name}'

    def get_tasks(self):
        all_tasks = {}
        # 1. Search for sequence classification tasks.
        seq_class_tasks = SequenceClassificationTask.query.filter_by(collection=self.id)
        all_tasks['SequenceClassification'] = list(seq_class_tasks)
        return all_tasks

    def get_unannotated_texts(self):
        all_texts = set(Text.query.filter_by(discarded=False, collection=self.id))
        annotated_texts = set(self.get_annotated_texts())
        unannotated_texts = all_texts - annotated_texts
        return list(sorted(unannotated_texts, key=lambda t: t.index))

    def get_annotated_texts(self):
        # TODO Refactor this as soon as new task-types are added.
        all_tasks = self.get_tasks()
        annotated_texts = set()
        for task_type, tasks in all_tasks.items():
            if task_type == 'SequenceClassification':
                for task in tasks:
                    query = list(
                        db.session.query(Text, SequenceClassificationAnnotation)
                            .filter(Text.id == SequenceClassificationAnnotation.text)
                            .filter(SequenceClassificationAnnotation.seq_task == task.id).all()
                    )
                    task_texts = [row[0] for row in query]
                    task_texts = set(task_texts)
                    annotated_texts.update(task_texts)
            # More Tasks here
        return list(sorted(annotated_texts, key=lambda t: t.index))

    def serialize_dict(self):
        data = {
            'Config': {
                'Name': self.name,
            }
        }
        # Serialiaize tasks
        all_tasks = list(flatten([list(tasks) for tasks in self.get_tasks().values()]))
        all_tasks_serialized = [task.serialize_dict() for task in all_tasks]
        data['Config']['Tasks'] = all_tasks_serialized

        # Get text and Annotations
        texts = Text.query.filter_by(collection=self.id)
        texts_serialized = []
        for text in texts:
            # Get annotations of texts
            annotations = []
            for task in all_tasks:
                # 1. Query for SeqClass Annotations
                seq_class_annotation = list(SequenceClassificationAnnotation.query \
                                            .filter_by(text=text.id, seq_task=task.id))
                annotations.extend([annotation.serialize_dict() for annotation in seq_class_annotation])
            text_serialized = text.serialize_dict()
            text_serialized['Annotations'] = annotations
            texts_serialized.append(text_serialized)
        data['Texts'] = texts_serialized
        return data


class Text(db.Model):
    __tablename__ = 'Text'
    id = db.Column(db.Integer, primary_key=True)
    collection = db.Column(db.Integer, db.ForeignKey('Collection.id'), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    discarded = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Text {self.content[:20]} from Collection {self.collection}'

    def serialize_dict(self):
        data = {
            'Text': self.content,
            'Discarded': self.discarded
        }
        return data


class SequenceClassificationTask(db.Model):
    __tablename__ = "SequenceClassificationTask"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    al_config = db.Column(db.Integer, db.ForeignKey('ActiveLearningConfigForSequenceClassification.id'))
    collection = db.Column(db.Integer, db.ForeignKey('Collection.id'), nullable=False)

    def get_class_labels(self):
        cls_entries = SeqClassificationTaskToClasses.query.filter_by(seq_class_task=self.id)
        return [c.class_label for c in cls_entries]

    def get_class_label(self, label_id):
        query = list(SeqClassificationTaskToClasses.query.filter_by(seq_class_task=self.id, id=label_id))
        if query:
            return query[0]
        return None

    def get_annotation(self, text):
        query = list(SequenceClassificationAnnotation.query.filter_by(seq_task=self.id, text=text.id))
        if query:
            return self.get_class_label(query[0].class_label)
        return None

    def serialize_dict(self):
        data = {
            'Type': 'SequenceClassification',
            'Name': self.name,
            'Description': self.description,
            'Classes': self.get_class_labels()
        }
        if self.al_config:
            data['ActiveLearning'] = ActiveLearningConfigForSequenceClassification \
                .query.get(self.al_config).serialize_dict()
        return data


class ActiveLearningConfigForSequenceClassification(db.Model):
    __tablename__ = "ActiveLearningConfigForSequenceClassification"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer, default=1, nullable=False)
    model_name = db.Column(db.String, nullable=False)

    def serialize_dict(self):
        data = {
            'Start': self.start,
            'ModelName': self.model_name
        }
        return data


class SeqClassificationTaskToClasses(db.Model):
    __tablename__ = "SeqClassificationTaskToClasses"
    id = db.Column(db.Integer, primary_key=True)
    seq_class_task = db.Column(db.Integer, db.ForeignKey('SequenceClassificationTask.id'), nullable=False)
    class_label = db.Column(db.String(120), nullable=False)


class SequenceClassificationAnnotation(db.Model):
    __tablename__ = "SequenceClassificationAnnotation"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Integer, db.ForeignKey('Text.id'))
    seq_task = db.Column(db.Integer, db.ForeignKey('SequenceClassificationTask.id'), nullable=False)
    class_label = db.Column(db.Integer, db.ForeignKey('SeqClassificationTaskToClasses.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize_dict(self):
        data = {
            'TaskName': SequenceClassificationTask.query.get(self.seq_task).name,
            'Class': SeqClassificationTaskToClasses.query.get(self.class_label).class_label
        }
        return data


class TextQueue(db.Model):
    __tablename__ = "TextQueque"
    id = db.Column(db.Integer, primary_key=True)
    collection = db.Column(db.Integer, db.ForeignKey('Collection.id'), nullable=False)
    text = db.Column(db.Integer, db.ForeignKey('Text.id'), unique=True)
