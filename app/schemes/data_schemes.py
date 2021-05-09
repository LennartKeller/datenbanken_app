from . import ma
from ..models.data_model import Corpus, Text

class CorpusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Corpus

class TextSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Text
        include_fk = True
    
class CategorySchema(ma.Schema):
    class Meta:
        fields = ("value",)

class LabelSchema(ma.Schema):
    class Meta:
        fields = ("value",)