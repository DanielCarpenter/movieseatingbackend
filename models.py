from flask import (Flask, render_template)
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'super secret key'

db = SQLAlchemy(app)
admin = Admin(app, name='movielog', template_mode='bootstrap3')


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title


class MoviesView(ModelView):
    can_delete = False
    page_size = 50


db.create_all()
admin.add_view(MoviesView(Movies, db.session))
# genre=db.
# category=db.Column(db.String(20))

# class genre(db.Model):
#   genre=db.Column(db.String(20))

# class actors(db.Model):
#   name=db.Column(db.String(20))
#   category=db.Column()

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=1)
