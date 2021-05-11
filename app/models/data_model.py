from datetime import datetime

from . import db


class Collection(db.Model):
    __tablename__ = 'Collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f'Corpus {self.name}'


class Text(db.Model):
    __tablename__ = 'Text'
    id = db.Column(db.Integer, primary_key=True)
    collection = db.Column(db.Integer, db.ForeignKey('Collection.id'), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'Text {self.text[:20]} from Corpus {self.corpus}'


class SequenceClassificationTask(db.Model):
    __tablename__ = "SequenceClassificationTask"
    id = db.Column(db.Integer, primary_key=True)
    al_config = db.Column(db.Integer, db.ForeignKey('ActiveLearningConfigForSequenceClassification.id'))
    collection = db.Column(db.Integer, db.ForeignKey('Collection.id'), nullable=False)


class ActiveLearningConfigForSequenceClassification(db.Model):
    __tablename__ = "ActiveLearningConfigForSequenceClassification"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer, default=1, nullable=False)
    model_path = db.Column(db.String, nullable=False)
    model_name = db.Column(db.String, nullable=False)


class SeqClassificationTaskToClasses(db.Model):
    __tablename__ = "SeqClassificationTaskToClasses"
    id = db.Column(db.Integer, primary_key=True)
    seq_class_task = db.Column(db.Integer, db.ForeignKey('SequenceClassificationTask.id'), nullable=False)
    class_label = db.Column(db.String(120), nullable=False)


class SequenceClassificationAnnotation(db.Model):
    __tablename__ = "SequenceClassificationAnnotation"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Integer, db.ForeignKey('Text.id'), unique=True)
    seq_task = db.Column(db.Integer, db.ForeignKey('SequenceClassificationTask.id'), nullable=False)
    class_label = db.Column(db.Integer, db.ForeignKey('SeqClassificationTaskToClasses.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
