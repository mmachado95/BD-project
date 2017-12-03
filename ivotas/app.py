from flask import Flask, request, redirect, render_template, url_for
from ivotas import models
from ivotas import forms


app = Flask(__name__)


@app.route("/")
def index():
    models.create_tables()
    models.seed_tables()
    organic_units = models.search_organic_unit()
    print(organic_units)

    users = models.search_user()

    return render_template('main.html', users=users)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/create', methods=['POST'])
def register_person():
    form = forms.RegisterUserForm(request.form)
    form.organic_unit.choices = models.search_organic_unit()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        organic_unit_id = form.organic_unit.data
        password = form.password.data
        contact = form.contact.data
        address = form.address.data
        cc = form.cc.data
        end_date = form.end_date.data
        type = form.type.data

        models.create_user(organic_unit_id, name, password, contact, address, cc, end_date, type)

        return redirect(url_for('admin'))
    return render_template('register_user.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
