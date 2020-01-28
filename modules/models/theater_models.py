from modules import db
from marshmallow_sqlalchemy import ModelSchema
from modules.models.movie_models import Movie

"Different Locations with theaters"
class Location(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20)) 
    address=db.Column(db.String(50))

    def __repr__(self):
        return "{} {}".format(self.name, self.address)

#Showing is the top level information record: everything related to a list of showings in a front end is available in this Model.


"A theater configurable in size for varied theater sizes"
class Theater(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rowNumber=db.Column(db.Integer) #for configurable theater sizes
    rowSize=db.Column(db.Integer)   #for configurable theater sizes
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', backref=db.backref('theater', lazy=True))
    seats = db.relationship('Seat', back_populates='theater', lazy=True)


    def __repr__(self):
        return "{}x{} Theater. id: {}".format(self.rowNumber, self.rowSize, self.id)


class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('showing', lazy=True))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    theater = db.relationship('Theater', backref=db.backref('showing', lazy=True))

    def __repr__(self):
        return "{} {} in Theater {}".format(self.time, self.movie, self.theater_id)


class Seat(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    number= db.Column(db.String(5), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    theater = db.relationship('Theater', back_populates='seats')
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', back_populates='reservations')

    def __repr__(self):
        return self.number

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable = False)
    showing_id = db.Column(db.Integer, db.ForeignKey('showing.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return str(self.id)






class TheaterSchema(ModelSchema):
    class Meta:
        model = Theater

class LocationSchema(ModelSchema):
    class Meta:
        model = Location

class ShowingSchema(ModelSchema):
    class Meta:
        model = Showing


showing_schema = ShowingSchema
showings_schema = ShowingSchema(many=True)


class SeatSchema(ModelSchema):
    class Meta:
        model = Seat

seat_schema = SeatSchema
seats_schema = SeatSchema(many=True)







#db.create_all()




theater_schema = TheaterSchema
theaters_schema = TheaterSchema(many=True)

location_schema = LocationSchema
locations_schema = LocationSchema(many=True)

