from flask_restful import Resource, reqparse
from .models import Showing, Seat, User, showing_schema, showings_schema
from flask import abort, jsonify
from modules import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.theaters import Theater, Location
from modules.movies import Movie


class OneShowing(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('showing_id', type=int, required=True)
        self.args = parser.parse_args()

        show = Showing.query.filter(Showing.id == self.args['showing_id']).first()
        if not show:
            return abort(404, 'Showing with id: {} does not exist in database.'.format(self.args['showing_id']))

        return jsonify(showing_schema.dump(show))

    #@jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=str, required=True),
        parser.add_argument('movie_id', type=int, required=True),
        parser.add_argument('theater_id', type=int, required=True)
        parser.add_argument('location_id', type=int, required=True)
        self.args = parser.parse_args()
        
        theater = Theater.query.filter(Theater.id == self.args['theater_id']).first()
        if not theater:
            return abort(404, 'Theater with id: {} does not exist in database.'.format(self.args['theater_id']))

        movie = Movie.query.filter(Movie.id == self.args['movie_id']).first()
        if not movie:
            return abort(404, 'Movie with id: {} does not exist in database.'.format(self.args['movie_id']))
        
        location = Location.query.filter(Location.id == self.args['location_id']).first()
        if not location:
            return abort(404, 'location with id: {} does not exist in database.'.format(self.args['movie_id']))

        size = theater.rowSize * theater.rowNumber
        
        show = Showing(
            time=self.args['time'],
            movie_id=self.args['movie_id'],
            theater_id=self.args['theater_id'],
            location_id=self.args['location_id']

        )


        try:
            db.session.add(show)
            db.session.commit()
        except:
            return abort(500, 'An error occurred while trying to add new Showing to database.')

        return jsonify(message='New Showing has been created.')


class ShowingList(Resource):

    #@jwt_required
    def get(self):
        shows = Showing.query.all()
        resp = jsonify(showings_schema.dump(shows))
        resp.status_code = 200
        return resp


class OneSeat(Resource):
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('seat_id', type=int, required=True),
        parser.add_argument('showing_id', type=int, required=True)
        #parser.add_argument('user_id', type=int, required=True)
        self.args = parser.parse_args()
        
        showing = Showing.query.filter(Showing.id == self.args['showing_id']).first()
        if not showing:
            return abort(404, 'Showing with id: {} does not exist in database.'.format(self.args['showing_id']))
        
        seat = Seat.query.filter(Seat.id == self.args['seat_id']).first()
        if seat.user_id != None:
            return abort(400, 'seat is reserved')
        
        seat.user_id = get_jwt_identity()
        
        
        
        

        try:
            db.session.add(seat)
            db.session.commit()
        except:
            return abort(500, 'error reserving seat')
        
        return jsonify(message='Seat reserved')
        

