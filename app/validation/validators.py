from cerberus import Validator
from .custom_types import ExistingPath

class DataReaderValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['existing_path'] = ExistingPath
