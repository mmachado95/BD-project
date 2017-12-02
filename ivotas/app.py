from flask import Flask, render_template
from ivotas import models


app = Flask(__name__)


@app.route("/")
def hello():
    models.create_tables()
    models.seed_tables()

    users = models.search_user()

    return render_template('main.html', users=users)


@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
