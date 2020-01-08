from modules import db
from marshmallow_sqlalchemy import ModelSchema

#Showing is the top level information record: everything related to a list of showings in a front end is available in this Model.
class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('showing', lazy=True))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    theater = db.relationship('Theater', backref=db.backref('showing', lazy=True))

    def __repr__(self):
        return "{} {} in Theater {}".format(self.time, movie, theater)


class Theater(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rowNumber=db.Column(db.Integer) #for configurable theater sizes
    rowSize=db.Column(db.Integer)   #for configurable theater sizes

    def __repr__(self):
        return self.id

class ShowingSchema(ModelSchema):
    class Meta:
        model = Showing

showing_schema = ShowingSchema


db.create_all()


