from modules import db
from ..theaters.models import Seat
from flask_security import UserMixin, RoleMixin
from marshmallow_sqlalchemy import ModelSchema

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

    def __str__(self):
        return self.email

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(email=username).first()
    
    #For registering new users via API
    @classmethod
    def nextId():
        next = User.query(db.func.max(User.id)).first()
        return (next.id+1)

db.create_all()

#flask marshmallow serializer
class UserSchema(ModelSchema):
    class Meta:
        model = User


users_schema = UserSchema(many=True)
user_schema = UserSchema()