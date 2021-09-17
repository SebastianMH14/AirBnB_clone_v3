#!/usr/bin/python3
"""the crud for the object states"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states():
    """return all the states"""
    if request.method == "GET":
        all_states = storage.all(State)
        list_all_states = []
        for state in all_states.values():
            list_all_states.append(state.to_dict())
        return jsonify(list_all_states)

    if request.method == "POST":
        if not request.json:
            abort(400, "Not a JSON")
        content = request.get_json()

        if "name" not in content.keys():
            abort(400, "Missing name")

        obj = State(name=content["name"])
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def states_id(state_id):
    """return states by id"""
    if request.method == "GET":
        states = storage.all(State)
        for value in states.values():
            if state_id == value.id:
                return jsonify(value.to_dict())
        abort(404)

    if request.method == "DELETE":
        states = storage.all(State)
        for value in states.values():
            if state_id == value.id:
                value.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == "PUT":
        states = storage.all(State)
        for obj in states.values():
            if state_id == obj.id:
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
