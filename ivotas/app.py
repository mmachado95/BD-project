from flask import Flask, request, redirect, render_template, url_for, g, session
from ivotas import models
from ivotas import forms
from ivotas import utils
from datetime import datetime

import click


app = Flask(__name__)
app.secret_key = b'\xe0\xbe]\xb3\x1eK"\xf2\xf1\xb9\xd0\xf8\xa8$\xdb\x9b\x89\xc1t>\xed\x86\xa4\x00'


"""
Safe close database connection
"""
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close

@app.cli.command()
def first_use():
    models.create_tables()
    models.seed_tables()


@app.route("/")
def index():
    return render_template('main.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        return render_template('admin.html')
    return redirect(url_for('login_admin'))


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    form = forms.AuthenticateUserForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user_id = models.search_user_by_username_and_password(username, password, True)
        if user_id is None:
            error = 'Authentication failed'
        else:
            session['username'] = username
            return redirect(url_for('admin'))

    return render_template('login_admin.html', form=form, error=error)


@app.route("/admin/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('admin'))


@app.route('/create_user', methods=['GET', 'POST'])
def register_person():
    error = None
    form = forms.RegisterUserForm(request.form)
    form.organic_unit.choices = models.get_organic_units(None, False)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        organic_unit_id = form.organic_unit.data
        password = form.password.data
        contact = form.contact.data
        address = form.address.data
        cc = form.cc.data
        end_date = form.end_date.data
        type = form.type.data
        is_admin= form.is_admin.data

        error = models.create_user(
            organic_unit_id,
            name,
            password,
            contact,
            address,
            cc,
            end_date,
            type,
            is_admin
        )
        if error:
            return render_template('register_user.html', form=form, error=error)
        return redirect(url_for('admin'))
    return render_template('register_user.html', form=form, error=error)


@app.route('/choose_user', methods=['GET', 'POST'])
def choose_person():
    form = forms.ChooseUserForm(request.form)
    form.user.choices = models.get_users(True, {'status': False})

    if request.method == 'POST' and form.validate():
        user = form.user.data
        return redirect(url_for('change_person', user_id=user))
    return render_template('choose_user.html', form=form)


@app.route('/change_user/<int:user_id>', methods=['GET', 'POST'])
def change_person(user_id):
    error = None
    form = forms.ChangeUserForm(request.form)

    # missing validators
    if request.method == 'POST' and utils.validate_user_change(form.name.data, form.password.data, form.contact.data, form.address.data, form.cc.data, form.end_date.data, form.type.data, form.is_admin.data):
        name = form.name.data
        password = form.password.data
        organic_unit_id = form.organic_unit.data
        contact = form.contact.data
        address = form.address.data
        cc = form.cc.data
        end_date = form.end_date.data
        type = form.type.data
        is_admin = form.is_admin.data

        error = models.update_user(
            str(user_id),
            unidade_organica_id=str(organic_unit_id),
            password=password,
            nome=name,
            contacto=contact,
            morada=address,
            cc=cc,
            data_validade=str(end_date),
            tipo=str(type),
            administrador=str(is_admin)
        )
        if error:
            user = models.search_user(user_id)
            form = forms.ChangeUserForm(request.form, organic_unit=user[1], type=user[7])
            form.organic_unit.choices = models.get_organic_units(None, None)
            form = utils.set_user_form_values(form, user)
            return render_template('change_user.html', form=form, error=error)

        return redirect(url_for('admin'))
    elif form.name.data is not None or form.organic_unit.choices is not None or form.password.data is not None or form.contact.data is not None or form.address.data is not None or form.cc.data is not None or form.end_date.data is not None or form.type.data is not None and form.is_admin.data is not None:
        error = 'Invalid input'

    user = models.search_user(user_id)
    form = forms.ChangeUserForm(request.form, organic_unit=user[1], type=user[7], is_admin=user[8])
    form.organic_unit.choices = models.get_organic_units(None, None)
    form = utils.set_user_form_values(form, user)

    return render_template('change_user.html', form=form, error=error)


@app.route('/manage_faculty', methods=['GET', 'POST'])
def manage_faculty():
    return render_template('manage_organic_unit.html', option='faculty')


@app.route('/manage_faculty/create', methods=['GET', 'POST'])
def create_faculty():
    form = forms.CreateFacultyForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        models.create_faculty(name)
        return redirect(url_for('manage_faculty'))

    return render_template('faculty_forms.html', form=form, option=1)


@app.route('/manage_faculty/change', methods=['GET', 'POST'])
def change_faculty():
    form = forms.ChangeFacultyForm(request.form)
    form.faculty.choices = models.get_faculties()

    if request.method == 'POST' and form.validate():
        id_to_update = form.faculty.data
        new_name = form.new_name.data
        models.update_organic_unit(id_to_update, nome=new_name)
        return redirect(url_for('manage_faculty'))
    return render_template('faculty_forms.html', form=form, option=2)


@app.route('/manage_faculty/delete', methods=['GET', 'POST'])
def delete_faculty():
    form = forms.DeleteFacultyForm(request.form)
    form.faculty.choices = models.get_faculties()

    if request.method == 'POST' and form.validate():
        id_to_delete = form.faculty.data
        departments_of_faculty = models.get_departments(str(id_to_delete))

        for department in departments_of_faculty:
            models.delete_data('UnidadeOrganica', department[0])

        models.delete_data('UnidadeOrganica', id_to_delete)
        return redirect(url_for('manage_faculty'))
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
        return redirect(url_for('manage_department'))

    return render_template('department_forms.html', form=form, option=1, current_faculty=None, current_name=None)


@app.route('/manage_department/choose', methods=['GET', 'POST'])
def choose_department():
    form = forms.ChooseDepartmentForm(request.form)
    form.department.choices = models.get_departments(None)

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
        return redirect(url_for('manage_department'))
    elif form.faculty.data is not None:
        error = 'Nome inválido'

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
    form.department.choices = models.get_departments(None)

    if request.method == 'POST' and form.validate():
        id_to_delete = form.department.data
        models.delete_data('UnidadeOrganica', id_to_delete)
        return redirect(url_for('manage_department'))
    return render_template('department_forms.html', form=form, option=4, current_faculty=None, current_name=None)


@app.route('/manage_voting_table', methods=['GET', 'POST'])
def manage_voting_table():
    return render_template('manage_voting_table.html')


@app.route('/manage_voting_table/create', methods=['GET', 'POST'])
def create_voting_table():
    form = forms.CreateVotingTableForm(request.form)
    form.election.choices = models.get_elections(False, False, True)
    form.organic_unit.choices = models.get_organic_units(None, True)

    if request.method == 'POST' and form.validate():
        election_id = form.election.data
        organic_unit_id = form.organic_unit.data
        models.create_voting_table(election_id, organic_unit_id)
        return redirect(url_for('manage_voting_table'))

    return render_template('voting_table_forms.html', form=form, option=1, current_election=None, current_organic_unit=None)


@app.route('/manage_voting_table/delete', methods=['GET', 'POST'])
def delete_voting_table():
    form = forms.DeleteVotingTableForm(request.form)
    form.voting_table.choices = models.get_voting_tables(True, False)

    if request.method == 'POST' and form.validate():
        voting_table_id = form.voting_table.data
        models.delete_data('MesaDeVoto', voting_table_id)
        return redirect(url_for('admin'))
    return render_template('voting_table_forms.html', form=form, option=4, current_election=None, current_organic_unit=None)


@app.route('/election/type', methods=['GET', 'POST'])
def choose_type():
    return render_template('choose_type_election.html')


@app.route('/election/create/<int:type>', methods=['GET', 'POST'])
def create_election(type):
    if type == 1:
        form = forms.CreateElectionWithoutOrganicUnitForm(request.form)
    else:
        form = forms.CreateElectionForm(request.form)
        form.organic_unit.choices = models.get_organic_units(type, False)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data

        start_date = form.start_date.data
        end_date = form.end_date.data
        if start_date > end_date:
            return render_template('create_election.html', form=form, error='Datas inválidas')

        if type == 1:
            models.create_election(name, description, start_date, end_date, str(type), None)
        else:
            organic_unit = form.organic_unit.data
            models.create_election(name, description, start_date, end_date, str(type), str(organic_unit))
        return redirect(url_for('admin'))

    return render_template('create_election.html', form=form, error=None, type=type)


@app.route('/election/choose', methods=['GET', 'POST'])
def choose_election():
    form = forms.ChooseElectionForm(request.form)
    form.election.choices = models.get_elections(False, True, False)

    if request.method == 'POST' and form.validate():
        election = form.election.data
        return redirect(url_for('change_election', election_id=election))
    return render_template('choose_election.html', form=form)


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

        models.update_election(election_id, nome=name, descricao=description, inicio=str(start_date), fim=str(end_date))
        return redirect(url_for('admin'))

    election = models.search_election(election_id, False)
    form.name.data = election[0]
    form.description.data = election[1]
    form.start_date.data = election[2]
    form.end_date.data = election[3]

    return render_template('change_election.html', form=form, error=None)


@app.route('/manage_candidate_list', methods=['GET', 'POST'])
def manage_candidate_list():
    return render_template('manage_candidate_list.html')


@app.route('/manage_candidate_list/create', methods=['GET', 'POST'])
def create_candidate_list():
    form = forms.CreateCandidateListForm(request.form)
    name_error = None

    if request.method == 'POST' and (form.name.data is not None) and (len(form.name.data) > 0 and len(form.name.data) < 100):
        name = form.name.data
        election = form.election.data
        list_id = models.create_list(election, name)
        if models.search_election(election, True)[0] == 1:
            return redirect(url_for('choose_list_type', election_id=election, list_id=list_id, list_type=1))
        else:
            return redirect(url_for('add_candidates', election_id=election, list_id=list_id))
    else:
        if form.name.data is not None and (len(form.name.data) <= 0 or len(form.name.data) >= 100):
            name_error = 'Invalid Name'

    form.election.choices = models.get_elections(False, True, False)
    return render_template('create_candidate_list.html', form=form, name_error=name_error)


@app.route('/manage_candidate_list/create/choose_list_type/<int:election_id>/<int:list_id>', methods=['GET', 'POST'])
def choose_list_type(election_id, list_id):
    return render_template('choose_list_type.html', election_id=election_id, list_id=list_id)


# Given the election type return the users that can apply to that election
def get_candidates_of_type(election_type, election_id, list_type):
    candidates = []

    if list_type is not None:
        candidates = models.get_users(False, {'status': True, 'type': list_type, 'id': election_id})
    elif election_type == 2:
        candidates = models.get_users(False, {'status': True, 'type': 3, 'id': election_id})
    elif election_type == 3:
        candidates = models.get_users(False, {'status': True, 'type': 1, 'id': election_id})
    elif election_type == 4:
        candidates = models.get_users(False, {'status': True, 'type': 1, 'id': election_id})

    return candidates


@app.route('/manage_candidate_list/create/<int:election_id>/<int:list_id>', methods=['GET', 'POST'], defaults={'list_type': None})
@app.route('/manage_candidate_list/create/<int:election_id>/<int:list_id>/<int:list_type>', methods=['GET', 'POST'])
def add_candidates(election_id, list_id, list_type):
    form = forms.AddCandidatesForm(request.form)
    election_type = models.search_election(election_id, True)
    form.candidates.choices = get_candidates_of_type(election_type[0], election_id, None)

    if request.method == 'POST' and form.candidates.data != None and len(form.candidates.data) > 0:
        candidates = form.candidates.data
        models.add_candidates(list_id, candidates)
        return redirect(url_for('manage_candidate_list'))

    form = forms.AddCandidatesForm(request.form)
    election_type = models.search_election(election_id, True)
    if list_type:
        form.candidates.choices = get_candidates_of_type(election_type[0], election_id, list_type)
    else:
        form.candidates.choices = get_candidates_of_type(election_type[0], election_id, None)

    return render_template('add_candidates.html', form=form)


@app.route('/manage_candidate_list/choose', methods=['GET', 'POST'])
def choose_candidate_list():
    form = forms.ChooseCandidateListForm(request.form)
    form.list.choices = models.get_lists(True)

    if request.method == 'POST' and form.validate():
        list = form.list.data
        return redirect(url_for('change_candidate_list', list_id=list))
    return render_template('choose_candidate_list.html', form=form)


@app.route('/manage_candidate_list/change/<int:list_id>', methods=['GET', 'POST'])
def change_candidate_list(list_id):
    name_error = None
    form = forms.ChangeCandidateListForm(request.form)

    if request.method == 'POST' and(form.name.data != None and form.candidates.data != None) and (len(form.name.data) > 0):
        election = form.election.data
        name = form.name.data
        models.update_list(list_id, eleicao_id=str(election), nome=name)
        return redirect(url_for('admin'))
    elif form.name.data != None and (len(form.name.data) <= 0 or len(form.name.data) >= 100):
        name_error = 'Invalid name'

    list = models.search_list(list_id)
    form = forms.ChangeCandidateListForm(request.form, election=list[1])
    form.election.choices = models.get_elections(False, True, False)
    form.name.data = list[2]

    return render_template('change_candidate_list.html', form=form, error=name_error, list_id=list_id)


@app.route('/manage_candidate_list/delete', methods=['GET', 'POST'])
def delete_candidate_list():
    form = forms.DeleteCandidateListForm(request.form)
    form.list.choices = models.get_lists(True)

    if request.method == 'POST' and form.validate():
        list = form.list.data
        models.delete_data('Lista', list)
        return redirect(url_for('admin'))
    return render_template('delete_candidate_list.html', form=form)


@app.route('/know_where_user_voted', methods=['GET', 'POST'])
def know_where_user_voted():
    form = forms.ChooseUserForm(request.form)
    form.user.choices = models.get_users(True, {'status': False})

    if request.method == 'POST' and form.validate():
        user_id = form.user.data
        return redirect(url_for('know_where_user_voted_choose_election', user_id=user_id))
    return render_template('know_where_user_voted.html', form=form)


@app.route('/know_where_user_voted/user_<int:user_id>/choose_election', methods=['GET', 'POST'])
def know_where_user_voted_choose_election(user_id):
    form = forms.ChooseElectionForm(request.form)
    form.election.choices = models.search_elections_that_user_voted(user_id)

    if request.method == 'POST' and form.validate():
        election_id = form.election.data
        return redirect(url_for('know_where_user_voted_end', user_id=user_id, election_id=election_id))
    return render_template('know_where_user_voted_choose_election.html', form=form)


@app.route('/know_where_user_voted/user_<int:user_id>/election_<int:election_id>', methods=['GET', 'POST'])
def know_where_user_voted_end(user_id, election_id):
    res = models.get_place_where_user_voted(user_id, election_id)
    print(user_id)
    print(election_id)
    print(res)
    place = res[0]
    moment = res[1]
    return render_template('know_where_user_voted_end.html', place=place, moment=moment)


@app.route('/details_of_past_elections', methods=['GET', 'POST'])
def details_of_past_elections():
    form = forms.ChooseElectionForm(request.form)
    form.election.choices = models.get_elections_past()

    if request.method == 'POST' and form.validate():
        election_id = form.election.data
        return redirect(url_for('details_of_past_elections_end', election_id=election_id))

    return render_template('details_of_past_elections.html', form=form)


@app.route('/details_of_past_elections/election_<int:election_id>', methods=['GET', 'POST'])
def details_of_past_elections_end(election_id):
    election = models.search_election(election_id, False)
    type_of_election = election[4]
    print(type_of_election)

    if type_of_election != 1:
        lists = models.search_lists_of_election(election_id, False)
        return render_template('details_of_past_elections_end.html', election=election, lists=lists)

    if type_of_election == 1:
        lists_of_alunos = models.search_lists_of_election_1(election_id, 3)
        lists_of_docentes = models.search_lists_of_election_1(election_id, 1)
        lists_of_funcionarios = models.search_lists_of_election_1(election_id, 2)
        print(lists_of_alunos)
        print(lists_of_docentes)
        print(lists_of_funcionarios)
        return render_template('details_of_past_elections_end_1.html', election=election,
        lists_of_alunos=lists_of_alunos, lists_of_docentes=lists_of_docentes, lists_of_funcionarios=lists_of_funcionarios)


@app.route('/voting_table_status', methods=['GET', 'POST'])
def voting_table_status():
    voting_tables = models.search_voting_tables_of_election()
    return render_template('voting_table_status.html', voting_tables=voting_tables)

# VOTE PAGES

@app.route('/choose_voting_table', methods=['GET', 'POST'])
def vote_choose_voting_table():
    form = forms.ChooseVotingTableForm(request.form)
    form.voting_table.choices = models.get_voting_tables(False, True)

    if request.method == 'POST' and form.validate():
        voting_table_id = form.voting_table.data
        return redirect(url_for('identify_user', voting_table_id=voting_table_id))

    return render_template('vote_choose_voting_table.html', form=form)


@app.route('/voting_table_<int:voting_table_id>/identify_user', methods=['GET', 'POST'])
def identify_user(voting_table_id):
    form = forms.IdentifyUserForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        field = form.field.data
        text = form.text.data
        users_ids = models.search_user_by_fields(field, text)

        if users_ids == []:
            error = 'No user found'
        else:
            voting_terminal_id = models.create_voting_terminal(str(voting_table_id))
            return redirect(url_for('authenticate_user', voting_table_id=voting_table_id, voting_terminal_id=voting_terminal_id, users_ids=users_ids))

    return render_template('vote_identify_user.html', form=form, voting_table_id=voting_table_id, error=error)


@app.route('/voting_table_<int:voting_table_id>/voting_terminal_<int:voting_terminal_id>/authenticate_user', methods=['GET', 'POST'])
def authenticate_user(voting_table_id, voting_terminal_id):
    users_ids = eval(request.args.get('users_ids'))
    form = forms.AuthenticateUserForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user_id = models.search_user_by_username_and_password(username, password, False)
        if user_id == None:
            error = 'Authentication failed'
        elif user_id[0] in users_ids:
            user_id = user_id[0]
            return redirect(url_for('vote', voting_table_id=voting_table_id, voting_terminal_id=voting_terminal_id, user_id=user_id))
        else:
            error = 'User not in identified users'

    return render_template('vote_authenticate_user.html', form=form, error=error)


def user_can_vote(user_type, election_type):
    if user_type == 1 and election_type == 2:
        return False
    if user_type == 2 and election_type != 1:
        return False
    if user_type == 3 and election_type != 1 and election_type != 2:
        return False
    return True


@app.route('/voting_table_<int:voting_table_id>/voting_terminal_<int:voting_terminal_id>/vote', methods=['GET', 'POST'])
def vote(voting_table_id, voting_terminal_id):
    user_id = eval(request.args.get('user_id'))

    voting_table = models.search_voting_table(voting_table_id)

    # Get Election id
    election_id = voting_table[1]
    election = models.search_election(election_id, False)
    election_end = election[3]
    election_type = election[4]

    # Get user type
    user_type = models.search_user(user_id)[7]

    # Get lists of election
    if election_type == 1:
        lists = models.search_candidates_lists_by_type(election_id, user_type)
    else:
        lists = models.search_lists_of_election(election_id, True)

    # Append Null and Blank votes
    lists.append((-1, 'Nulo'))
    lists.append((0, 'Branco'))

    form = forms.ChooseCandidateListForm(request.form)
    form.list.choices = lists
    error = None

    if request.method == 'POST' and form.validate():
        list = form.list.data

        users_votes_in_election = models.check_user_vote_in_election(user_id, election_id)

        current_time = datetime.now()

        # Election has ended
        if election_end < current_time:
            error = 'You cant vote. Election has already ended.'
            return render_template('vote_choose_list.html', form=form, error=error)
        # User has already voted
        elif users_votes_in_election != []:
            error = 'You have already voted in election.'
            return render_template('vote_choose_list.html', form=form, error=error)
        # User can't vote on this election
        elif not user_can_vote(user_type, election_type):
            print("entered here")
            error = 'You can´t vote in this election'
            return render_template('vote_choose_list.html', form=form, error=error)
        else:
            # Create vote
            models.create_vote(user_id, voting_table_id)

            # update total votes
            total_votes = int(election[5])
            total_votes += 1

            # Null Vote
            if list == -1:
                # update null votes
                null_votes = int(election[7])
                null_votes += 1
                models.update_election(election_id, total_votos=str(total_votes), votos_nulos=str(null_votes))
            # Blank vote
            elif list == 0:
                # update blank votes
                blank_votes = int(election[6])
                blank_votes += 1
                models.update_election(election_id, total_votos=str(total_votes), votos_brancos=str(blank_votes))
            # Counter of list
            else:
                list_chosen = models.search_list(list)
                list_votes = list_chosen[3]
                list_votes += 1
                models.update_election(election_id, total_votos=str(total_votes))
                models.update_list(list, numero_votos=str(list_votes))
        return redirect(url_for('index'))
    return render_template('vote_choose_list.html', form=form, error=error)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
