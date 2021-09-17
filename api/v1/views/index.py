#!/usr/bin/python3
"""creating the routes for the api"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def status_api():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count_obj():
    obj_stats = {}
    for key, value in classes.items():
        count = storage.count(value)
        obj_stats[key] = count
    return jsonify(obj_stats)
