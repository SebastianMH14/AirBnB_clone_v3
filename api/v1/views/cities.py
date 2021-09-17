#!/usr/bin/python3
"""the CRUD for City object"""
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage
from models import city
from models.city import City
from models.state import State
from flask import jsonify, request


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET", "POST"])
def city_states(state_id):
    """retrives all the cities in a state"""
    if request.method == "GET":
        all_states = storage.all(State)
        for state in all_states.values():
            if state_id == state.id:
                list_all_cities = []
                for city in state.cities:
                    list_all_cities.append(city.to_dict())
                return jsonify(list_all_cities)
        abort(404)

    if request.method == "POST":
        all_states = storage.all(State)
        for state in all_states.values():
            if state_id == state.id:
                if not request.json:
                    abort(400, "Not a JSON")
                content = request.get_json()

                if "name" not in content.keys():
                    abort(400, "Missing name")
                obj = City(name=content["name"], state_id=state_id)
                obj.save()
                return jsonify(obj.to_dict()), 201
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def cities(city_id):
    """retives the cities"""
    if request.method == "GET":
        cities = storage.all(City)
        for value in cities.values():
            if city_id == value.id:
                return jsonify(value.to_dict())
        abort(404)

    if request.method == "DELETE":
        cities = storage.all(City)
        for value in cities.values():
            if city_id == value.id:
                value.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == "PUT":
        cities = storage.all(City)
        for obj in cities.values():
            if city_id == obj.id:
                if not request.json:
                    abort(400, "Not a JSON")
                content = request.get_json()

                for key, value in content.items():
                    if key == 'id':
                        continue
                    if key == 'updated_at' or key == 'created_at':
                        continue
                    else:
                        setattr(obj, key, value)
                obj.save()
                return jsonify(obj.to_dict()), 200
        abort(404)
