from flask import Flask, request, redirect, render_template, url_for, g
from ivotas import models
from ivotas import forms


app = Flask(__name__)


"""
Safe close database connection
"""
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close


@app.route("/")
def index():
    models.create_tables()
    models.seed_tables()
    return render_template('main.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/create_user', methods=['GET', 'POST'])
def register_person():
    form = forms.RegisterUserForm(request.form)
    form.organic_unit.choices = models.get_organic_units()

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

    return render_template('department_forms.html', form=form, option=1, current_faculty=None, current_name=None)


@app.route('/manage_department/choose', methods=['GET', 'POST'])
def choose_department():
    form = forms.ChooseDepartmentForm(request.form)
    form.department.choices = models.get_departments()

    if request.method == 'POST' and form.validate():
        id_to_update = form.department.data
        return redirect(url_for('change_department', department_id=id_to_update))
    return render_template('department_forms.html', form=form, option=2, current_faculty=None, current_name=None)


@app.route('/manage_department/change/<int:department_id>', methods=['GET', 'POST'])
def change_department(department_id):
    form = forms.ChangeDepartmentForm(request.form)
    error = None

    if request.method == 'POST' and (len(form.name.data) > 0 and len(form.name.data) < 100):
        faculty_id = form.faculty.data
        name = form.name.data
        models.update_organic_unit(department_id, nome=name)
        models.update_department(department_id, faculdade_id=str(faculty_id))
        return redirect(url_for('admin'))
    elif form.faculty.data != None or form.faculty.data != None:
        error = 'Nome inválido'

    # TODO optimize this
    department = models.search_department(department_id)
    department_name = department[1]
    faculty_name = models.search_organic_unit(department[0])
    faculties = models.get_faculties()

    form = forms.ChangeDepartmentForm(request.form, faculty=department[0])
    form.faculty.choices = faculties
    form.name.data = department_name
    return render_template('department_forms.html', form=form, option=3, error=error)


@app.route('/manage_department/delete', methods=['GET', 'POST'])
def delete_department():
    form = forms.DeleteDepartmentForm(request.form)
    form.department.choices = models.get_departments()

    if request.method == 'POST' and form.validate():
        id_to_delete = form.department.data
        models.delete_data('unidade_organica', id_to_delete)
        return redirect(url_for('admin'))
    return render_template('department_forms.html', form=form, option=4, current_faculty=None, current_name=None)


@app.route('/manage_voting_table', methods=['GET', 'POST'])
def manage_voting_table():
    return render_template('manage_voting_table.html')


@app.route('/manage_voting_table/create', methods=['GET', 'POST'])
def create_voting_table():
    form = forms.CreateVotingTableForm(request.form)
    form.election.choices = models.get_elections(True)
    form.organic_unit.choices = models.get_organic_units()

    if request.method == 'POST' and form.validate():
        election_id = form.election.data
        organic_unit_id = form.organic_unit.data
        models.create_voting_table(election_id, organic_unit_id)
        return redirect(url_for('admin'))

    return render_template('voting_table_forms.html', form=form, option=1, current_election=None, current_organic_unit=None)


@app.route('/manage_voting_table/choose', methods=['GET', 'POST'])
def choose_voting_table():
    form = forms.ChooseVotingTableForm(request.form)
    form.voting_table.choices = models.get_voting_tables(True)

    if request.method == 'POST' and form.validate():
        id_to_update = form.voting_table.data
        return redirect(url_for('change_voting_table', voting_table_id=id_to_update))
    return render_template('voting_table_forms.html', form=form, option=2, current_election=None, current_organic_unit=None)


@app.route('/manage_voting_table/change/<int:voting_table_id>', methods=['GET', 'POST'])
def change_voting_table(voting_table_id):
    # TODO normalmente valida-se mas neste caso nçao deixa idk why
    form = forms.ChangeVotingTableForm(request.form)

    if request.method == 'POST':
        election = form.election.data
        organic_unit = form.organic_unit.data
        models.update_voting_table(voting_table_id, eleicao_id=str(election), unidade_organica_id=str(organic_unit))
        return redirect(url_for('admin'))

    # TODO check if field has changed
    voting_table = models.search_voting_table(voting_table_id, True, False)

    election_id = voting_table[1]
    organic_unit_id = voting_table[2]
    election = voting_table[3]
    organic_unit = voting_table[4]

    form = forms.ChangeVotingTableForm(election=election_id, organic_unit=organic_unit_id)
    form.election.choices = models.get_elections(True)
    form.organic_unit.choices = models.get_organic_units()

    return render_template('voting_table_forms.html', form=form, option=3, current_election=election, current_organic_unit=organic_unit)


# TODO Check if election is happening with this voting table
@app.route('/manage_voting_table/delete', methods=['GET', 'POST'])
def delete_voting_table():
    form = forms.DeleteVotingTableForm(request.form)
    form.voting_table.choices = models.get_voting_tables(True)

    if request.method == 'POST' and form.validate():
        voting_table_id = form.voting_table.data
        models.delete_data('mesa_de_voto', voting_table_id)
        return redirect(url_for('admin'))
    return render_template('voting_table_forms.html', form=form, option=4, current_election=None, current_organic_unit=None)


@app.route('/election/create', methods=['GET', 'POST'])
def create_election():
    form = forms.CreateElectionForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data

        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date > end_date:
            return render_template('create_election.html', form=form, error='Datas inválidas')

        type = form.type.data

        models.create_election(name, description, start_date, end_date, type)
        return redirect(url_for('admin'))
    return render_template('create_election.html', form=form, error=None)


@app.route('/election/choose', methods=['GET', 'POST'])
def choose_election():
    form = forms.ChooseElectionForm(request.form)
    form.election.choices = models.get_elections(True)

    if request.method == 'POST' and form.validate():
        election = form.election.data
        return redirect(url_for('change_election', election_id=election))
    return render_template('choose_election.html', form=form)


# TODO check if election is already running
@app.route('/election/change/<int:election_id>', methods=['GET', 'POST'])
def change_election(election_id):
    form = forms.ChangeElectionForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data

        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date > end_date:
            return render_template('change_election.html', form=form, error='Datas inválidas')

        type = form.type.data

        models.update_election(election_id, nome=name, descricao=description, inicio=str(start_date), fim=str(end_date), tipo=str(type))
        return redirect(url_for('admin'))

    election = models.search_election(election_id)
    form.name.data = election[0]
    form.description.data = election[1]
    form.start_date.data = election[2]
    form.end_date.data = election[3]
    form.type.data = election[4]

    return render_template('change_election.html', form=form, error=None)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
