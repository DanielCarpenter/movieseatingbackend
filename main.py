from modules import app
# from flask_basicauth import BasicAuth
#
# basic_auth = BasicAuth(app)
# @app.route('/')
# @basic_auth.required
# def movieLog():
#     return 'Movie Log!!!'


if __name__=='__main__':
    app.run(debug=True)
