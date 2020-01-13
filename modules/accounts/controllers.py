from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required)
from flask_security.utils import verify_password, encrypt_password
from modules import db
import datetime
from modules.accounts import User, Role




#code from here: https://blog.tecladocode.com/jwt-authentication-and-token-refreshing-in-rest-apis/
class ApiLogin(Resource):
    # defining the request parser and expected arguments in the request
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

    def post(self):
        data = self.parser.parse_args()
        # read from database to find the user and then check the password
        user = User.find_by_username(data['username'])
        if user and verify_password(data['password'], user.password):
            # when authenticated, return a fresh access token and a refresh token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'token': access_token,
                'refresh': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


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
        self.args = self.parser.parse_args()
        if(User.find_by_username(self.args['username'])): #if user exists dont allow
            return {"message": "User with {} username already exists".format(self.args['username'])}, 409
        else:
            #create the user with provided parameters, and automatically set it as active, hashes password
            user = User(
                first_name = self.args['firstName'],
                last_name = self.args['lastName'],
                email = self.args['username'],
                password = encrypt_password(self.args['password']),
                active = True,
                confirmed_at = datetime.datetime.now()
            )
            try:
                db.session.add(user)
                db.session.commit()
            except:
                return {"message": "User database error!"}, 500
            return {"message": "{} user created!"}, 200
