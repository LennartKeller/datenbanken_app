from . import ma
from ..models.data_model import *


class CollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Collection


class TextSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Text
        include_fk = True
