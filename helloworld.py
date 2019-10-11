from flask import (Flask, render_template)
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.update(dict(secret_key="wrong"))
#db = SQLAlchemy(app)
admin = Admin(app)

@app.route('/')
def home():
    return render_template('home.html', hello="Get off my lawn!")

#class User(db.Model):
 #   name = db.Column(db.String(20))



if __name__ == '__main__':
    app.run(debug=1)