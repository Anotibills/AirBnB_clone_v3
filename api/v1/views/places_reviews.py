#!/usr/bin/python3
"""
Script that creates Create a new view for Review object
that handles all default RESTful API
"""

from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def handle_reviews(place_id=None, review_id=None):
    '''The method handler for the reviews endpoint'''
    handlers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in handlers:
        return handlers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_reviews(place_id=None, review_id=None):
    '''This gets the review with the given id'''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            reviews = [review.to_dict() for review in place.reviews]
            return jsonify(reviews)
    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
    raise NotFound()


def add_review(place_id=None, review_id=None):
    '''This adds a new review'''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        raise NotFound()
    if 'text' not in data:
        raise BadRequest(description='Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def remove_review(place_id=None, review_id=None):
    '''This removes a review with the given id'''
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def update_review(place_id=None, review_id=None):
    '''this updates the review with the given id'''
    xkeys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            data = request.get_json()
            if not isinstance(data, dict):
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    raise NotFound()
