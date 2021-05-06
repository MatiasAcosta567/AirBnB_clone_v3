#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)


@app.route('/status')
def index():
    return jsonify({'status': 'OK'})