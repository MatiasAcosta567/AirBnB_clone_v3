#!/usr/bin/python3
"""First time API"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def context(self):
    storage.close()


@app.errorhandler(404)
def handle_invalid_usage(error):
    response = {
        'error': "Not found"
    }
    return jsonify(response), 404


if __name__ == '__main__':
    my_port = getenv('HBNB_API_PORT', 5000)
    my_host = getenv('HBNB_API_HOST', '0.0.0.0')
    app.run(host=my_host, port=my_port, threaded=True)
