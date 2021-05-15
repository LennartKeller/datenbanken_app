from app import app
from app.models import Collection
import json
if __name__ == '__main__':
    with app.app_context():
        c = Collection.query.all()[0]
        with open('test-output.json', 'w') as f:
            json.dump(c.serialize_dict(), f, indent=4)
