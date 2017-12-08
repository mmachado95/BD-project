import psycopg2
from flask import g

"""
Future documentation purposes:
->http://flask.pocoo.org/docs/0.12/tutorial/dbcon/
"""


"""
Connect to database
"""
def connect_db(_host, _dbname, _user, _password):
    conn = None
    try:
        conn = psycopg2.connect(host=_host, dbname=_dbname, user=_user, password=_password)
    except(Exception, psycopg2.DatabaseError) as error:
        print('Unable to connect to database %s' % error)
    return conn


"""
Safe get  connection to dabase
"""
def get_db(dbname):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db('localhost', dbname, 'Machado', '')
    return db


"""
Parse sql file for commands to run
"""
def get_commands(filename):
    f = open(filename, 'r')
    commands = f.read()
    return commands.split(';')


"""
Takes keyword args received by functions and returns a search string ready to be executed
"""
def get_search_statement(table, args):
    search_statement = 'SELECT * FROM ' + table

    # If no search arguments where received
    if args != {}:
        search_statement += ' WHERE '
    else:
        return search_statement

    # Query options
    for key, value in args.items():
        search_statement += key + '=' + "'" + value + "'"

    return search_statement


def get_update_statement(table, id_to_update, args):
    first_iter = True
    update_statement = 'UPDATE ' + table + ' SET '
    id_to_update = str(id_to_update)

    for key, value in args.items():
        if not first_iter:
            update_statement += ", "
        update_statement += key + '=' + "'" + value + "'"
        first_iter = False

    if table == 'faculdade' or table == 'departamento':
        update_statement += ' WHERE unidade_organica_id=' + "'" + id_to_update + "'"
    else:
        update_statement += ' WHERE id=' + "'" + id_to_update + "'"

    print(update_statement)
    return update_statement


def set_user_form_values(form, user):
    form.name.data = user[2]
    form.contact.data = user[3]
    form.address.data = user[4]
    form.cc.data = user[5]
    form.end_date.data = user[6]
    form.type.choices = [(1, 'Professor'), (2, 'Funcionário'), (3, 'Estudante')]
    return form


def validate_user_change(name, contact, address, cc, end_date, type, is_admin):
    if name is None or (len(name) <= 1 or len(name) >= 100):
        return False
    if contact is None or (len(contact) <= 1 or len(contact) >= 100):
        return False
    if address is None or (len(address) <= 1 or len(address) >= 100):
        return False
    if cc is None or (len(cc) <= 1 or len(cc) >= 10):
        return False
    if end_date is None:
        return False
    if type is None:
        return False
    if is_admin is None:
        return False
    return True
