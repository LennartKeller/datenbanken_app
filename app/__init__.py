import os
from pathlib import Path

from flask import Flask, current_app, send_file, jsonify

from .api import api_bp
from .client import client_bp
from .models import db, Collection
from .schemes import ma

# This file contains the code to initialize the backend-application.

app = Flask(__name__, static_folder='../dist/static')
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

from .config import Config

app.logger.info('>>> {}'.format(Config.FLASK_ENV))

db.init_app(app)
ma.init_app(app)


@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


@app.route('/debug')
def debug():
    return {'status': {'running': True}}
