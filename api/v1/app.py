#!/usr/bin/python3
"""First time API"""


from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def context():
    storage.close()


if __name__ == '__main__':
    if (getenv('HBNB_API_HOST') != None):
        my_host = getenv('HBNB_API_HOST')
    else:
        my_host = '0.0.0.0'
    if (getenv('HBNB_API_PORT') != None):
        my_port = getenv(('HBNB_API_PORT'))
    else:
        my_port = 5000
    app.run(host=my_host, port=my_port,threaded=True)