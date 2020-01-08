from modules import db


#Showing is the top level information record: everything related to a list of showings in a front end is available in this Model.
class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(10), nullable=False)
    movie = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)

    def __repr__(self):
        movie = Movie.query.get(self.movie)
        return "{} {} in Theater {}".format(self.time, movie.title, theater)


class Theater(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    rowNumber=db.Column(db.Integer) #for configurable theater sizes
    rowSize=db.Column(db.Integer)   #for configurable theater sizes

    def __repr__(self):
        return self.id




db.create_all()
