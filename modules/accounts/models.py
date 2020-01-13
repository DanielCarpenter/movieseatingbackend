from modules import db
from flask_security import UserMixin, RoleMixin
from marshmallow_sqlalchemy import ModelSchema
from modules.theaters import Location, Theater

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    reservations = db.relationship('Seat',back_populates='user', lazy=True)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(email=username).first()
        
    def __str__(self):
        return self.email
    
class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('showing', lazy=True))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    theater = db.relationship('Theater', backref=db.backref('showing', lazy=True))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    location = db.relationship('Location', backref=db.backref('showing', lazy=True))
    seats = db.relationship('Seat', back_populates='showing', lazy=True)

    def __repr__(self):
        return "{} {} in Theater {}".format(self.time, self.movie, self.theater_id)


class Seat(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    number= db.Column(db.Integer, nullable=False)
    showing_id = db.Column(db.Integer, db.ForeignKey('showing.id'), nullable=False)
    showing = db.relationship('Showing', back_populates='seats')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='reservations')


    def __repr__(self):
        return "Seat {}, reserved: {}".format(self.number, reserved = bool(self.user_id))
 

    


db.create_all()

#flask marshmallow serializer
class UserSchema(ModelSchema):
    class Meta:
        model = User


users_schema = UserSchema(many=True)
user_schema = UserSchema()


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
