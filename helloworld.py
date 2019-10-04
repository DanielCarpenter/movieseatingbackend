from flask import (Flask, render_template)

app = Flask(__name__)
app.config.update(dict(secret_key="wrong"))


@app.route('/')
def home():
    return render_template('home.html', hello="Get off my lawn!")


if __name__ == '__main__':
    app.run(debug=1)
