#!/usr/bin/python3
"""the crud for amenity"""
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage
from flask import jsonify, request
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
def amenities():
    """get the amenities objects"""
    if request.method == "GET":
        amenities = storage.all(Amenity)
        list_all_amenities = []
        for amenty in amenities.values():
            list_all_amenities.append(amenty.to_dict())
        return jsonify(list_all_amenities)

    if request.method == "POST":
        if not request.json:
            abort(400, "Not a JSON")
        content = request.get_json()
        if "name" not in content.keys():
            abort(400, "Missing name")
        obj = Amenity(name=content["name"])
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenity_id(amenity_id):
    """delete, put, and get objects of amenities"""
    if request.method == "GET":
        all_amenities = storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity_id == amenity.id:
                return jsonify(amenity.to_dict())
        abort(404)

    if request.method == "DELETE":
        all_amenities = storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity_id == amenity.id:
                amenity.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == "PUT":
        all_amenities = storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity_id == amenity.id:
                if not request.json:
                    abort(400, "Not a JSON")
                content = request.get_json()
                for key, value in content.items():
                    if key == "id":
                        continue
                    elif key == 'updated_at' or key == 'created_at':
                        continue
                    else:
                        setattr(amenity, key, value)
                amenity.save()
                return jsonify(amenity.to_dict()), 200
        abort(404)
