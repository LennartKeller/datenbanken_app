from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .data_model import Corpus, Text