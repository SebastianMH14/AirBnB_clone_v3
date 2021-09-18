#!/usr/bin/python3
"""The CRUD for the Review"""
from models.review import Review
from models.user import User
from models.place import Place
from werkzeug.exceptions import abort
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET", "POST"])
def reviews(place_id):
    """create and read all teh reviews"""
    if request.method == "GET":
        place = storage.get(Place, place_id)
        if place is not None:
            list_all_review = []
            for reviews in place.reviews:
                list_all_review.append(reviews.to_dict())
            return jsonify(list_all_review)
        abort(404)

    if request.method == "POST":
        place = storage.get(Place, place_id)
        if place is not None:
            if not request.json:
                abort(400, "Not a JSON")
            content = request.get_json()
            if "user_id" not in content.keys():
                abort(400, "Missing user_id")
            user = storage.get(User, content["user_id"])
            if user is not None:
                if "text" not in content.keys():
                    abort(400, "Missing text")
                obj = Review(
                    text=content["text"], user_id=content["user_id"],
                    place_id=place_id)
                obj.save()
                return jsonify(obj.to_dict()), 201
            else:
                abort(404)
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def review_id(review_id):
    """retrives, delete and updated an updated obj review"""
    if request.method == "GET":
        review = storage.get(Review, review_id)
        if review is not None:
            return jsonify(review.to_dict())
        else:
            abort(404)

    if request.method == "DELETE":
        review = storage.get(Review, review_id)
        if review is not None:
            review.delete()
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    if request.method == "PUT":
        review = storage.get(Review, review_id)
        if review is not None:
            if not request.json:
                abort(400, "Not a JSON")

            content = request.get_json()
            for key, value in content.items():
                if "id" == key:
                    continue
                elif "user_id" == key or "place_id" == key:
                    continue
                elif "created_at" == key or "updated_at" == key:
                    continue
                else:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
        abort(404)
