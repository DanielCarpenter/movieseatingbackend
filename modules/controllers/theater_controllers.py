from flask_restful import Resource, reqparse
from modules.models.user_models import  User
from flask import abort, jsonify
from modules import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.models.theater_models import Theater, Showing, Seat, Reservation, reservations_schema
from modules.models.user_models import User


class Reservations(Resource):
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('showing_id', type=int, required=True)
        parser.add_argument('seats', action='append', type=int, required=True)
        self.args = parser.parse_args()

        show = Showing.query.filter(Showing.id == self.args['showing_id']).first()
        if not show:
            return abort(404, 'Showing with id: {} does not exist in database.'.format(self.args['showing_id']))
        
        for seat in self.args['seats']:
            if Reservation.query.filter(Reservation.seat_id == seat, Reservation.showing_id == self.args['showing_id']).first() is not None:
                return abort(400, "We're Sorry, some seats you selected are no longer available!")
        
        for seat in self.args['seats']:
            try:
                db.session.add(
                    Reservation(
                        seat_id = seat,
                        showing_id = self.args['showing_id'],
                        user_id = get_jwt_identity()
                    )
                )
                db.session.commit()
            except:
                return abort(500, "error: could not add reservation to database")
        
        return jsonify("Seats successfully reserved")

    @jwt_required
    def get(self):
        return jsonify(reservations_schema.dump(Reservation.query.filter(Reservation.user_id == get_jwt_identity())))



            

            
        
        
