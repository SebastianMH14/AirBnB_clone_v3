#!/usr/bin/python3
"""the crud for the user object"""
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage
from flask import jsonify, request
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users():
    """get user objects"""
    if request.method == "GET":
        users = storage.all(User)
        list_all_users = []
        for value in users.values():
            list_all_users.append(value.to_dict())
        return jsonify(list_all_users)

    if request.method == "POST":
        if not request.json:
            abort(400, "Not a JSON")
        content = request.get_json()
        if "email" not in content.keys():
            abort(400, "Missing email")
        if "password" not in content.keys():
            abort(400, "Missing password")
        obj = User(email=content["email"], password=content["password"])
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def users_id(user_id):
    """get user object by id"""
    if request.method == "GET":
        users = storage.all(User)
        for user in users.values():
            if user_id == user.id:
                return jsonify(user.to_dict())
        abort(404)

    if request.method == "DELETE":
        users = storage.all(User)
        for user in users.values():
            if user_id == user.id:
                user.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)

    if request.method == "PUT":
        users = storage.all(User)
        for user in users.values():
            if user_id == user.id:
                if not request.json:
                    abort(400, "Not a JSON")
                content = request.get_json()
                for key, value in content.items():
                    if key == "id" or key == "email":
                        continue
                    elif key == "created_at" or key == "updated_at":
                        continue
                    else:
                        setattr(user, key, value)
                user.save()
                return jsonify(user.to_dict()), 200
        abort(404)
