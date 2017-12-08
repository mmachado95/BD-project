from flask import Flask, request, redirect, render_template, url_for, g, session
from ivotas import models
from ivotas import forms
import time
from datetime import datetime


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
    #models.create_tables()
    #models.seed_tables()
    return render_template('main.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/create_user', methods=['GET', 'POST'])
def register_person():
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
    elif form.faculty.data != None:
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


# TODO only list organic units it can be place on
@app.route('/manage_voting_table/create', methods=['GET', 'POST'])
def create_voting_table():
    form = forms.CreateVotingTableForm(request.form)
    form.election.choices = models.get_elections(True, False)
    form.organic_unit.choices = models.get_organic_units(None, True)

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
    form.election.choices = models.get_elections(True, False)
    form.organic_unit.choices = models.get_organic_units(None, True)

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
    form.election.choices = models.get_elections(False, True)

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


#TODO refactor this, old code the candidates error doesnt happen anymore
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

    form.election.choices = models.get_elections(False, True)
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
        return redirect(url_for('admin'))

    form = forms.AddCandidatesForm(request.form)
    election_type = models.search_election(election_id, True)
    if list_type:
        form.candidates.choices = get_candidates_of_type(election_type[0], election_id, list_type)
    else:
        form.candidates.choices = get_candidates_of_type(election_type[0], election_id, None)

    return render_template('add_candidates.html', form=form)


# TODO only allow selecting lists on elections that aren't happening
@app.route('/manage_candidate_list/choose', methods=['GET', 'POST'])
def choose_candidate_list():
    form = forms.ChooseCandidateListForm(request.form)
    form.list.choices = models.get_lists(True)

    if request.method == 'POST' and form.validate():
        list = form.list.data
        return redirect(url_for('change_candidate_list', list_id=list))
    return render_template('choose_candidate_list.html', form=form)


# TODO only allow selecting lists on elections that aren't happening
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
    form.election.choices = models.get_elections(False, True)
    form.name.data = list[2]

    return render_template('change_candidate_list.html', form=form, error=name_error, list_id=list_id)


# TODO only allow selecting lists on elections that aren't happening
@app.route('/manage_candidate_list/delete', methods=['GET', 'POST'])
def delete_candidate_list():
    form = forms.DeleteCandidateListForm(request.form)
    form.list.choices = models.get_lists(True)

    if request.method == 'POST' and form.validate():
        list = form.list.data
        models.delete_data('lista', list)
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
    place = models.get_place_where_user_voted(user_id, election_id)[0]
    return render_template('know_where_user_voted_end.html', place=place)


@app.route('/choose_voting_table', methods=['GET', 'POST'])
def vote_choose_voting_table():
    form = forms.ChooseVotingTableForm(request.form)
    form.voting_table.choices = models.get_voting_tables(True)

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
        voting_terminal_id = "1"

        if users_ids == []:
            error = 'No user found'
        else:
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
        user_id = models.search_user_by_username_and_password(username, password)
        if user_id == None:
            error = 'Authentication failed'
        elif user_id[0] in users_ids:
            user_id = user_id[0]
            return redirect(url_for('vote', voting_table_id=voting_table_id, voting_terminal_id=voting_terminal_id, user_id=user_id))
        else:
            error = 'User not in identified users'

    return render_template('vote_authenticate_user.html', form=form, error=error)


@app.route('/voting_table_<int:voting_table_id>/voting_terminal_<int:voting_terminal_id>/vote', methods=['GET', 'POST'])
def vote(voting_table_id, voting_terminal_id):
    user_id = eval(request.args.get('user_id'))

    voting_table = models.search_voting_table(voting_table_id)

    # Get Election id
    election_id = voting_table[1]

    # Get lists of election
    lists = models.search_lists_of_election(election_id)

    # Append Null and Blank votes
    lists.append((-1, 'Nulo'))
    lists.append((0, 'Branco'))

    form = forms.ChooseCandidateListForm(request.form)
    form.list.choices = lists
    error = None

    if request.method == 'POST' and form.validate():
        list = form.list.data

        election = models.search_election(election_id, False)
        election_end = election[3]
        current_time = datetime.fromtimestamp(time.time())

        users_votes_in_election = models.check_user_vote_in_election(user_id, election_id)

        # Election has ended
        if election_end < current_time:
            error = 'You cant vote. Election has already ended.'
            return render_template('vote_choose_list.html', form=form, error=error)
        # User has already voted
        elif users_votes_in_election != []:
            error = 'You have already voted in election.'
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
