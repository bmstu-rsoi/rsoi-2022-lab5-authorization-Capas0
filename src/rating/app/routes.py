from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from .auth import authorized
from .base import db
from .models import Rating
from .schemas import RatingSchema

api = Blueprint('api', __name__)


def format_errors(messages):
    for field, errors in messages.items():
        for error in errors:
            yield {'field': field, 'error': error}


def format_validation_error(text, error):
    return {
        'message': text,
        'errors': list(format_errors(error.messages))
    }


def parse_args(username):
    data = request.json
    data['username'] = username
    args = RatingSchema().load(data)
    args['stars'] = min(100, max(1, args.get('stars', 1)))
    return args


@api.route('/rating', methods=['PATCH'])
@authorized(username=True)
def edit_rating(username):
    try:
        args = parse_args(username)
        try:
            rating = db.session.execute(
                db.select(Rating).where(Rating.username == args['username'])
            ).scalars().first()
        except DataError:
            rating = Rating(**args)
            db.session.add(rating)
        rating.stars = args['stars']
        db.session.commit()
        return jsonify(RatingSchema().dump(rating)), 200
    except ValidationError as err:
        return jsonify(format_validation_error('Invalid data', err)), 400


@api.route('/rating', methods=['GET'])
@authorized(username=True)
def get_rating(username):
    rating = db.session.execute(
        db.select(Rating).where(Rating.username == username)
    ).scalars().first()
    if rating is None:
        rating = Rating(username=username, stars=1)
        db.session.add(rating)
        db.session.commit()

    return jsonify(RatingSchema().dump(rating)), 200
