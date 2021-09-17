#!/usr/bin/python3
"""creating the routes for the api"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_api():
    return jsonify({"status": "OK"})
