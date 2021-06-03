from cerberus import Validator
from pathlib import Path


class DataReaderValidator(Validator):

    def _validate_path_exists(self, constraint, field, value):
        "{'type': 'boolean'}"
        if constraint is True and not Path(value).exists():
            self._error(field, 'Path has to point to an existing file.')

    def get_error_messages(self):
        if not self.errors:
            return ''
        return '\n'.join([f'Error in field: {field}: {" ".join(messages)}' for field, messages in self.errors.items()])


class DataReaderValidationException(Exception):
    pass
