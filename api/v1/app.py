#!/usr/bin/python3
"""creating an api"""

from api.v1.views import app_views
from flask import Flask
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def restart_data(exception):
    """close session so the new data is outputed"""
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000

    app.run(debug=True, host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
