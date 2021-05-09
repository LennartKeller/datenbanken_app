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
    sequence_annotation_config = db.Column(
        db.Integer, db.ForeignKey('SequenceAnnotationConfig.id'),
        nullable=False)


class ActiveLearningConfig(db.Model):
    __tablename__ = "ActiveLearningConfig"
    id = db.Column(db.Integer, primary_key=True)
    estimator_path = db.Column(db.String, nullable=False)
    estimator_name = db.Column(db.String, nullable=False)
    task = db.Column(db.String, nullable=False)
    objective = db.Column(db.String, nullable=False)

class SequenceAnnotationConfig(db.Model):
    __tablename__ = "SequenceAnnotationConfig"
    id = db.Column(db.Integer, primary_key=True)


class Estimator(db.Model):
    __tablename__ = "Estimator"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)



class Label(db.Model):
    __tablename__ = "Label"
    id = db.Column(db.Integer, primary_key=True)
    sequence_annotation_config = db.Column(
        db.Integer, db.ForeignKey('SequenceAnnotationConfig.id'))
    value = db.Column(db.String, nullable=False)


class Category(db.Model):
    __tablename__ = "Category"
    id = db.Column(db.Integer, primary_key=True)
    sequence_annotation_config = db.Column(
        db.Integer, db.ForeignKey('SequenceAnnotationConfig.id'))
    value = db.Column(db.String, nullable=False)


# Relationships

class TextToLabel(db.Model):
    __tablename__ = 'TextToLabel'
    text_id = db.Column(db.Integer, db.ForeignKey('Text.id'), primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey('Label.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Label")

class TextToCategory(db.Model):
    __tablename__ = 'TextToCategory'
    text_id = db.Column(db.Integer, db.ForeignKey('Text.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    child = db.relationship("Category")

class ProjectToCorpus(db.Model):
    __tablename__ = 'CorpusToProject'
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), primary_key=True)
    corpus_id = db.Column(db.Integer, db.ForeignKey('Corpus.id'), primary_key=True)

class SequenceAnnotationConfigToLabel(db.Model):
    __tablename__ = 'SequenceAnnotationConfigToLabel'
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer, db.ForeignKey('SequenceAnnotationConfig.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('Label.id'))

class SequenceAnnotationConfigToCategory(db.Model):
    __tablename__ = 'SequenceAnnotationConfigToCategoryl'
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer, db.ForeignKey('SequenceAnnotationConfig.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))