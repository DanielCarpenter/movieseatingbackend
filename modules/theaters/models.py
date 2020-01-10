from modules import db
from marshmallow_sqlalchemy import ModelSchema

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

    def __repr__(self):
        return "{}x{} Theater. id: {}".format(self.rowNumber, self.rowSize, self.id)





class TheaterSchema(ModelSchema):
    class Meta:
        model = Theater

class LocationSchema(ModelSchema):
    class Meta:
        model = Location







db.create_all()




theater_schema = TheaterSchema
theaters_schema = TheaterSchema(many=True)

location_schema = LocationSchema
locations_schema = LocationSchema(many=True)

