#!/usr/bin/python3
"""The CRUD for the Place objects"""
from api.v1.views.users import users_id
from models.user import User
from models.city import City
from models.place import Place
from werkzeug.exceptions import abort
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET", "POST"])
def places(city_id):
    """GET the places and create new ones"""
    if request.method == "GET":
        cities = storage.all(City)
        for city in cities.values():
            if city_id == city.id:
                list_all_place = []
                for place in city.places:
                    list_all_place.append(place.to_dict())
                return jsonify(list_all_place)
        abort(404)

    if request.method == "POST":
        cities = storage.all(City)
        for city in cities.values():
            if city_id == city.id:
                if not request.json:
                    abort(400, "Not a JSON")

                content = request.get_json()
                if "user_id" not in content.keys():
                    abort(400, "Missing user_id")
                users = storage.all(User)
                for user in users.values():
                    if content["user_id"] == user.id:
                        if "name" not in content.keys():
                            abort(400, "Missing name")
                        obj = Place(
                            user_id=content["user_id"], name=content["name"],
                            city_id=city_id)
                        obj.save()
                        return jsonify(obj.to_dict()), 201
                abort(404)
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def places_id(place_id):
    """Update, read and delete obj of place by id"""
    if request.method == "GET":
        places = storage.all(Place)
        for place in places.values():
            if place_id == place.id:
                return jsonify(place.to_dict())
        abort(404)

    if request.method == "DELETE":
        places = storage.all(Place)
        for place in places.values():
            if place_id == place.id:
                place.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == "PUT":
        places = storage.all(Place)
        for place in places.values():
            if place_id == place.id:
                if not request.json:
                    abort(400, "Not a JSON")

                content = request.get_json()
                for key, value in content.items():
                    if "id" == key:
                        continue
                    elif "user_id" == key or "city_id" == key:
                        continue
                    elif "created_at" == key or "updated_at" == key:
                        continue
                    else:
                        setattr(place, key, value)
                place.save()
                return jsonify(place.to_dict()), 200
        abort(404)
