from flask_restful import Resource, reqparse
from .models import Movie, movie_schema, movies_schema
from flask import abort, jsonify
from modules import db
from flask_jwt_extended import jwt_required


class OneMovie(Resource):

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('movie_id', type=int, required=True)
        self.args = parser.parse_args()

        movie = Movie.query.filter(Movie.id == self.args['movie_id']).first()
        if not movie:
            return abort(404, 'Movie with id: {} does not exist in database.'.format(self.args['movie_id']))

        return jsonify(movies=movie_schema.dump(movie))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True),
        parser.add_argument('genre_id', type=int, required=True),
        parser.add_argument('cast_id', action='append', type=str)
        self.args = parser.parse_args()

        title = self.args['title']
        genre_id = self.args['genre_id']

        existing_movie = Movie.query.filter(Movie.title == title).first()
        if existing_movie:
            return abort(400, 'Movie with title: {} already exists in database.'.format(self.args['title']))

        movie = Movie(
            title=title,
            genre_id=genre_id
        )

        if self.args['cast_id']:
            for id in self.args['cast_id']:
                actor = Actor.query.filter(Actor.id == id).first()
                if not actor:
                    return abort(404, 'Actor with id: {} does not exist in database.'.format(id))
                movie.cast.append(actor)
                db.session.commit()

        try:
            db.session.add(movie)
            db.session.commit()
        except:
            return abort(500, 'An error occurred while trying to add new movie to database.')

        return jsonify(message='New movie has been created.')


class MovieList(Resource):

    @jwt_required
    def get(self):
        movies = Movie.query.all()

        return jsonify(movie=movies_schema.dump(movies))
