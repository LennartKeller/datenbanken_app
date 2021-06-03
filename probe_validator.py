from app.validation.validators import DataReaderValidator
from app.validation.validation_schemes import READER_CONFIG_SCHEMA

if __name__ == '__main__':
    validator = DataReaderValidator(READER_CONFIG_SCHEMA)
    cfg = {'Separator': '\n\n', 'Path': 'IMDBCollection.py'}
    validator(cfg)
