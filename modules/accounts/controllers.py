from flask_restful import Resource, reqparse
from flask import jsonify
from modules import db
import datetime
from modules.accounts import User, Role

class ApiRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('firstName',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('lastName',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = self.parser.parse_args()
        if(User.find_by_username(data['username'])):
            return {"message": "User with {} username already exists".format(data['username'])}, 409
        else:
            user = User(
                id = User.nextId(),
                first_name = self.args['firstName'],
                last_name = self.args['lastName'],
                email = self.args['username'],
                password = self.args['password'],
                confirmed_at = datetime.datetime()
                #Role = 'customer'
            )
            try:
                db.session.add(user)
                db.session.commit()
            except:
                return {"message": "User database error!"}, 500
            return {"message": "{} user created!"}, 200
