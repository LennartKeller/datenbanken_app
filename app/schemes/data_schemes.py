from . import ma
from ..models.data_model import Corpus, Text

class CorpusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Corpus

class TextSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Text
        include_fk = True