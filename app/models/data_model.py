from . import db
from datetime import datetime

class Corpus(db.Model):
    __tablename__ = 'Corpus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f'Corpus {self.name}'

class Text(db.Model):
    __tablename__ = 'Text'
    id = db.Column(db.Integer, primary_key=True)
    corpus = db.Column(db.Integer, db.ForeignKey('Corpus.id'), nullable=False)
    index = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'Text {self.text[:20]} from Corpus {self.corpus}'

class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    active_learning_config = db.Column(
        db.Integer, db.ForeignKey('ActiveLearningConfig.id'),
        nullable=False)


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False)


class Label(db.Model):
    __tablename__ = 'Label'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False)


class ActiveLearningConfig(db.Model):
    __tablename__ = "ActiveLearningConfig"
    id = db.Column(db.Integer, primary_key=True)
    estimator = db.Column(db.Integer, db.ForeignKey('Estimator.id'), nullable=False)
    begin = db.Column(db.Integer(), default=1, nullable=False)


class Estimator(db.Model):
    __tablename__ = "Estimator"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)


class SequenceAnnotation(db.Model):
    __tablename__ = 'SequenceAnnotation'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    created = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('Estimator.id'))
    labels = db.relationship("SequenceAnnotationToLabel")


# Relationships

class SequenceAnnotationToLabel(db.Model):
    __tablename__ = 'SequenceAnnotationToLabel'
    sequence_annoation_id = db.Column(db.Integer, db.ForeignKey('SequenceAnnotation.id'), primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey('Label.id'), primary_key=True)
    child = db.relationship("Label")


class ProjectToCorpus(db.Model):
    __tablename__ = 'CorpusToProject'
    project_annoation_id = db.Column(db.Integer, db.ForeignKey('Project.id'), primary_key=True)
    corpus_id = db.Column(db.Integer, db.ForeignKey('Corpus.id'), primary_key=True)
    child = db.relationship("Corpus")
