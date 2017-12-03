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


@app.route('/create_user', methods=['GET', 'POST'])
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


@app.route('/manage_faculty', methods=['GET', 'POST'])
def manage_faculty():
    return render_template('manage_organic_unit.html', option='faculty')


@app.route('/manage_faculty/create', methods=['GET', 'POST'])
def create_faculty():
    form = forms.CreateFacultyForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        models.create_faculty(name)
        return redirect(url_for('admin'))

    return render_template('faculty_forms.html', form=form, option=1)


@app.route('/manage_faculty/change', methods=['GET', 'POST'])
def change_faculty():
    form = forms.ChangeFacultyForm(request.form)
    form.faculty.choices = models.get_faculties()

    if request.method == 'POST' and form.validate():
        id_to_update = form.faculty.data
        new_name = form.new_name.data
        models.update_organic_unit(id_to_update, nome=new_name)
        return redirect(url_for('admin'))
    return render_template('faculty_forms.html', form=form, option=2)


@app.route('/manage_faculty/delete', methods=['GET', 'POST'])
def delete_faculty():
    form = forms.DeleteFacultyForm(request.form)
    form.faculty.choices = models.get_faculties()

    if request.method == 'POST' and form.validate():
        id_to_delete = form.faculty.data
        models.delete_data('unidade_organica', id_to_delete)
        return redirect(url_for('admin'))
    return render_template('faculty_forms.html', form=form, option=3)


@app.route('/manage_department', methods=['GET', 'POST'])
def manage_department():
    return render_template('manage_organic_unit.html', option='department')


@app.route('/manage_department/create', methods=['GET', 'POST'])
def create_department():
    form = forms.CreateDepartmentForm(request.form)
    form.faculty.choices = models.get_faculties()

    if request.method == 'POST' and form.validate():
        faculty_id = form.faculty.data
        name = form.name.data
        models.create_department(name, faculty_id)
        return redirect(url_for('admin'))

    return render_template('department_forms.html', form=form, option=1)


@app.route('/manage_department/change', methods=['GET', 'POST'])
def change_department():
    form = forms.ChangeDepartmentForm(request.form)
    form.department.choices = models.get_departments()

    if request.method == 'POST' and form.validate():
        id_to_update = form.department.data
        new_name = form.new_name.data
        models.update_organic_unit(id_to_update, nome=new_name)
        return redirect(url_for('admin'))
    return render_template('department_forms.html', form=form, option=2)


@app.route('/manage_department/delete', methods=['GET', 'POST'])
def delete_department():
    form = forms.DeleteDepartmentForm(request.form)
    form.department.choices = models.get_departments()

    if request.method == 'POST' and form.validate():
        id_to_delete = form.department.data
        models.delete_data('unidade_organica', id_to_delete)
        return redirect(url_for('admin'))
    return render_template('department_forms.html', form=form, option=3)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
