from flask import Flask
from ivotas import models
app = Flask(__name__)


@app.route("/")
def hello():
    models.create_tables()
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
