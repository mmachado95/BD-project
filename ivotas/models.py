import psycopg2
import datetime
from ivotas.utils import get_db, get_commands, get_search_statement, get_update_statement


"""
Create tables at startup
"""
def create_tables():
    commands = get_commands('ivotas/create_tables.sql')

    conn = None
    try:
        cur = get_db('ivotas').cursor()

        # create table one by one
        for command in commands:
            # empty line or comment
            if command.strip() != '' or command[0:2]=='--':
                cur.execute(command)

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Seed tables with test values
"""
def seed_tables():
    commands = get_commands('ivotas/seeds.sql')

    conn = None
    try:
        cur = get_db('ivotas').cursor()

        # create table one by one
        for command in commands:
            if command.strip() != '':
                cur.execute(command)

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


#################################
### Create records functions  ###
#################################

"""
Create new faculty
"""
def create_faculty(name):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # create organic_unit
        insert_statement = '''INSERT INTO UnidadeOrganica(nome) VALUES(%s) RETURNING id'''
        cur.execute(insert_statement, (name,))
        organic_unit_id = cur.fetchone()[0]

        # insert faculty in table
        insert_statement = '''INSERT INTO Faculdade(unidade_organica_id) VALUES(%s)'''
        cur.execute(insert_statement, (organic_unit_id,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new department
"""
def create_department(name, faculty_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # create organic_unit
        insert_statement = '''INSERT INTO UnidadeOrganica(nome) VALUES(%s) RETURNING id'''
        cur.execute(insert_statement, (name,))
        organic_unit_id = cur.fetchone()[0]

        # insert department in table
        insert_statement = '''
            INSERT INTO Departamento(unidade_organica_id, faculdade_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (organic_unit_id, faculty_id,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new user
"""
def create_user(organic_unit_id, name, password, contact, address, cc, end_date, type, is_admin):
    error = None
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert user in table
        insert_statement = '''
            INSERT INTO Pessoa(unidade_organica_id, nome, password, contacto, morada, cc, data_validade, tipo, administrador)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(insert_statement, (organic_unit_id, name, password, contact, address, cc, end_date, type, is_admin,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
        error = 'That cc already exists'
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()

    return error


"""
Create new election
"""
def create_election(name, description, start, finished, type, organic_unit):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert election in table
        if organic_unit is not None:
            insert_statement = '''
                INSERT INTO Eleicao(unidade_organica_id, nome, descricao, inicio, fim, tipo)
                VALUES(%s, %s, %s, %s, %s, %s)
            '''
            cur.execute(insert_statement, (organic_unit, name, description, start, finished, type,))
        else:
            insert_statement = '''
                INSERT INTO Eleicao(nome, descricao, inicio, fim, tipo)
                VALUES(%s, %s, %s, %s, %s)
            '''
            cur.execute(insert_statement, (name, description, start, finished, type,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new list for election
"""
def create_list(election_id, name):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list
        insert_statement = '''
            INSERT INTO Lista(eleicao_id, nome)
            VALUES(%s, %s)
            RETURNING id
        '''
        cur.execute(insert_statement, (election_id, name,))

        # fetch id that was inserted
        list_id = cur.fetchone()[0]

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()
    finally:
        # close communication with the PostgreSQL database server
        if cur is not None:
            cur.close()
        return list_id


def add_candidates(list_id, users_ids):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list
        insert_statement = '''
            INSERT INTO ListaDeCandidatos(lista_id, pessoa_id)
            VALUES(%s, %s)
        '''

        # add users to list
        for user_id in users_ids:
            cur.execute(insert_statement, (str(list_id), str(user_id)))
        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new voting table
"""
def create_voting_table(election_id, organic_unit_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert voting table
        insert_statement = '''
            INSERT INTO MesaDeVoto(eleicao_id, unidade_organica_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (election_id, organic_unit_id,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new voting terminal
"""
def create_voting_terminal(voting_table_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert voting terminal
        insert_statement = '''
            INSERT INTO TerminalDeVoto(mesa_de_voto_id)
            VALUES(%s)
        '''
        cur.execute(insert_statement, (voting_table_id,))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Create new vote
"""
def create_vote(user_id, voting_table_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert vote
        insert_statement = '''
            INSERT INTO Voto(pessoa_id, mesa_de_voto_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (user_id, voting_table_id))

        # commit the changes
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


########################
### Query functions ###
########################


"""
Get organic units
"""
def get_organic_units(type, dep_without_voting_tables):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get organic units
        if type is not None and type != 2:
            if type == 3:
                search_statement = '''
                    SELECT id, nome
                    FROM UnidadeOrganica, Faculdade
                    WHERE id=unidade_organica_id
                '''
                cur.execute(search_statement)
            elif type == 4:
                search_statement = '''
                    SELECT id, nome
                    FROM UnidadeOrganica, Departamento
                    WHERE id=unidade_organica_id
                '''
                cur.execute(search_statement)
        elif dep_without_voting_tables:
            now = datetime.datetime.now()
            search_statement = '''
                SELECT distinct(id), nome
                FROM UnidadeOrganica uo, Departamento d, Faculdade f
                WHERE uo.id=f.unidade_organica_id OR uo.id=d.unidade_organica_id
                AND id != ALL(
                    select distinct(mv.unidade_organica_id)
                    from MesaDeVoto mv, Eleicao e
                    where mv.eleicao_id=e.id and e.fim > timestamp %s
                )
            '''
            cur.execute(search_statement, (now,))
        else:
            search_statement = '''
                SELECT id, nome
                FROM UnidadeOrganica
            '''
            cur.execute(search_statement)

        organic_units = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return organic_units

"""
Get faculties
"""
def get_faculties():
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get faculties
        search_statement = '''
            SELECT id, nome
            FROM UnidadeOrganica, Faculdade
            WHERE id=unidade_organica_id
        '''
        cur.execute(search_statement)
        faculties = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return faculties


"""
Get departments
"""
def get_departments(of_faculty):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get departments
        if of_faculty is not None:
            search_statement = '''
                SELECT id
                FROM UnidadeOrganica, Departamento
                WHERE id=unidade_organica_id AND faculdade_id=%s
                GROUP BY id
            '''
            cur.execute(search_statement, (of_faculty,))
        else:
            search_statement = '''
                SELECT id, nome
                FROM UnidadeOrganica, Departamento
                WHERE id=unidade_organica_id
            '''
            cur.execute(search_statement)
        departments = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return departments


"""
Get elections
"""
def get_elections(form_friendly, future_elections, future_and_present_elections):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get elections
        if form_friendly:
            search_statement = '''
                SELECT id, nome
                FROM Eleicao
            '''
            cur.execute(search_statement)
        elif future_elections:
            now = datetime.datetime.now()
            search_statement = '''
                SELECT id, nome
                FROM Eleicao
                where inicio > timestamp %s;
            '''
            cur.execute(search_statement, (now,))
        elif future_and_present_elections:
            now = datetime.datetime.now()
            search_statement = '''
                SELECT id, nome
                FROM Eleicao
                where inicio > timestamp %s or fim > timestamp %s;
            '''
            cur.execute(search_statement, (now, now,))
        else:
            search_statement = '''
                SELECT *
                FROM Eleicao

            '''
            cur.execute(search_statement)

        elections = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return elections


"""
Get elections in the past
"""
def get_elections_past():
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        now = datetime.datetime.now()
        search_statement = '''
            SELECT id, nome
            FROM Eleicao
            where fim < timestamp %s;
        '''

        cur.execute(search_statement, (now,))
        elections = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return elections


"""
Get voting tables
"""
def get_voting_tables(form_friendly, to_vote):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get voting talbles
        if form_friendly:
            search_statement = '''
                SELECT mv.id, e.nome || ' ' || uo.nome
                FROM MesaDeVoto mv, Eleicao e, UnidadeOrganica uo
                WHERE mv.eleicao_id=e.id and mv.unidade_organica_id=uo.id
            '''
            cur.execute(search_statement)
        elif to_vote:
            now = datetime.datetime.now()
            search_statement = '''
                SELECT mv.id, e.nome || ' ' || uo.nome
                FROM MesaDeVoto mv, Eleicao e, UnidadeOrganica uo
                WHERE mv.eleicao_id=e.id and mv.unidade_organica_id=uo.id and e.fim > timestamp %s
            '''
            cur.execute(search_statement, (now,))
        else:
            search_statement = '''
                SELECT *
                FROM Eleicao
            '''
            cur.execute(search_statement)
        elections = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return elections


"""
Get Lists
"""
def get_lists(form_friendly):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get lists
        if form_friendly:
            search_statement = '''
                SELECT id, nome
                FROM Lista
            '''
        else:
            search_statement = '''
                SELECT *
                FROM Lista
            '''
        cur.execute(search_statement)
        lists = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return lists


"""
Get users
"""
def get_users(form_friendly, by_type):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get users
        if form_friendly:
            search_statement = '''
                SELECT id, 'Nome: ' || nome || ' ' || 'CC: ' || cc "Identificador"
                FROM Pessoa
            '''
            cur.execute(search_statement)
        elif by_type['status']:
            search_statement = '''
                SELECT p.id, 'Nome: ' || p.nome || ' ' || 'CC: ' || p.cc "Identificador"
                FROM Pessoa p
                WHERE tipo=%s
                AND id!=all(
                    select lc.pessoa_id
                    from Lista l, ListaDeCandidatos lc
                    where lc.lista_id=l.id and l.eleicao_id=%s
                )
            '''
            cur.execute(search_statement, (by_type['type'], by_type['id'],))
        else:
            search_statement = '''
                SELECT *
                FROM Pessoa
            '''
            cur.execute(search_statement)
        users = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return users


"""
Get users
"""
def get_list_of_candidates(election_id):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT *
            FROM ListaDeCandidatos
        '''
        cur.execute(search_statement)
        candidates = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return []
    else:
        return candidates


"""
Search organic unit based on id
"""
def search_organic_unit(organic_unit_id):
    organic_unit_id = str(organic_unit_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # search organic unit
        search_statement = '''
            SELECT nome
            FROM UnidadeOrganica
            WHERE id=%s
        '''
        cur.execute(search_statement, (organic_unit_id,))
        organic_unit = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return organic_unit

"""
Search department based on id
"""
def search_department(department_id):
    department_id = str(department_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # search department
        search_statement = '''
            SELECT faculdade_id, nome
            FROM UnidadeOrganica, Departamento
            WHERE id=unidade_organica_id and id=%s
        '''
        cur.execute(search_statement, (department_id,))
        department = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return department


"""
Search voting table based on id
"""
def search_voting_table(voting_table_id, names, election_date):
    voting_table_id = str(voting_table_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # search voting_table
        if names:
            search_statement = '''
                SELECT mv.id, mv.eleicao_id, mv.unidade_organica_id, e.nome "Eleicao", uo.nome "Unidade Organica"
                FROM MesaDeVoto mv, Eleicao e, UnidadeOrganica uo
                WHERE mv.eleicao_id=e.id and mv.unidade_organica_id=uo.id and mv.id=%s
            '''
        elif election_date:
            search_statement = '''
                SELECT inicio, fim
                FROM MesaDeVoto mv, Eleicao e
                WHERE mv.eleicao_id=e.id and e.id=%s
            '''
        else:
            search_statement = '''
                SELECT eleicao_id, unidade_organica_id
                FROM MesaDeVoto
                WHERE id=%s
            '''

        cur.execute(search_statement, (voting_table_id,))
        voting_table = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return voting_table


"""
Search election by id
"""
def search_election(election_id, returns_type):
    election_id = str(election_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        if returns_type:
            search_statement = '''
                SELECT tipo
                FROM Eleicao
                WHERE id=%s
            '''
        else:
            search_statement = '''
                SELECT nome, descricao, inicio, fim, tipo, total_votos, votos_brancos, votos_nulos
                FROM Eleicao
                WHERE id=%s
            '''

        cur.execute(search_statement, (election_id,))
        election = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return election



"""
Search list by id
"""
def search_list(list_id):
    list_id = str(list_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT id, eleicao_id, nome, numero_votos
            FROM Lista
            WHERE id=%s
        '''

        cur.execute(search_statement, (list_id,))
        list = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return list


"""
Search voting table by id
"""
def search_voting_table(voting_table_id):
    voting_table_id = str(voting_table_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT id, eleicao_id, unidade_organica_id
            FROM MesaDeVoto
            WHERE id=%s
        '''

        cur.execute(search_statement, (voting_table_id,))
        voting_table = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return voting_table


"""
Search elections that user voted
"""
def search_elections_that_user_voted(user_id):
    user_id = str(user_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT e.id, e.nome
            FROM Eleicao e, MesaDeVoto mv, Pessoa p, Voto v
            WHERE p.id=%s AND p.id=v.id AND v.mesa_de_voto_id=mv.id and mv.eleicao_id=e.id
        '''

        cur.execute(search_statement, (user_id,))
        elections_ids = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return elections_ids


"""
Search person by id
"""
def search_user(user_id):
    user_id = str(user_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT id, unidade_organica_id, nome, contacto, morada, cc, data_validade, tipo, administrador
            FROM Pessoa
            WHERE id=%s
        '''

        cur.execute(search_statement, (user_id,))
        user = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return user


"""
Search person by other fields
"""
def search_user_by_fields(field_type, field_text):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # Search by name
        if field_type == 1:
            search_statement = '''
                SELECT id
                FROM Pessoa
                WHERE nome=%s
            '''

        # Search by CC
        if field_type == 2:
            search_statement = '''
                SELECT id
                FROM Pessoa
                WHERE cc=%s
            '''

        cur.execute(search_statement, (field_text,))
        user = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return user


"""
Search person by username and password
"""
def search_user_by_username_and_password(nome, password, is_admin):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()
        user = None

        if is_admin:
            search_statement = '''
                SELECT id
                FROM Pessoa
                WHERE nome=%s AND password=%s AND administrador IS TRUE
            '''
        else:
            search_statement = '''
                SELECT id
                FROM Pessoa
                WHERE nome=%s AND password=%s
            '''
        cur.execute(search_statement, (nome, password,))
        user = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return user


"""
Search lists by election id
"""
def search_lists_of_election(election_id, form_friendly):
    election_id = str(election_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        if form_friendly:
            search_statement = '''
                SELECT id, nome
                FROM Lista
                WHERE eleicao_id=%s
            '''

        else:
            search_statement = '''
                SELECT nome, numero_votos
                FROM Lista
                WHERE eleicao_id=%s
            '''

        cur.execute(search_statement, (election_id,))
        lists = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return lists


"""
Search lists by election id
"""
def get_place_where_user_voted(user_id, election_id):
    election_id = str(election_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT uo.nome
            FROM UnidadeOrganica uo, Eleicao e, MesaDeVoto mv, Voto v, Pessoa p
            WHERE mv.eleicao_id=e.id AND mv.id=v.mesa_de_voto_id AND mv.unidade_organica_id=uo.id AND v.pessoa_id=p.id AND p.id=%s AND e.id=%s
        '''

        cur.execute(search_statement, (user_id, election_id,))
        place = cur.fetchone()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return place


########################
### Update functions ###
########################


"""
Update Organic Unit
"""
def update_organic_unit(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update faculty
        update_statement = get_update_statement('UnidadeOrganica', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Update Department
"""
def update_department(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update Department
        update_statement = get_update_statement('Departamento', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Update user
"""
def update_user(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    error = None

    # connect to database
    cur = get_db('ivotas').cursor()

    try:
        # update user
        update_statement = get_update_statement('Pessoa', id_to_update, kwargs)
        cur.execute(update_statement)

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
        error = 'That cc already exists'
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()

    return error


"""
Update election
"""
def update_election(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update election
        update_statement = get_update_statement('Eleicao', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Update list
"""
def update_list(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update list
        update_statement = get_update_statement('Lista', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


"""
Update voting table
"""
def update_voting_table(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update voting table
        update_statement = get_update_statement('MesaDeVoto', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except psycopg2.IntegrityError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


########################
### Delete functions ###
########################

"""
General delete function
"""
def delete_data(table, id_to_delete):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # delete
        if table == 'ListaDeCandidatos':
            delete_statement = 'DELETE FROM ' + table + ' WHERE pessoa_id=%s'
        else:
            delete_statement = 'DELETE FROM ' + table + ' WHERE id=%s'
        cur.execute(delete_statement, (id_to_delete,))

        # commit change
        get_db('ivotas').commit()

    except psycopg2.DatabaseError as e:
        get_db('ivotas').rollback()
    else:
        get_db('ivotas').commit()

    # close communication with the PostgreSQL database server
    if cur is not None:
        cur.close()


def check_user_vote_in_election(user_id, election_id):
    election_id = str(election_id)
    user_id = str(user_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT p.id
            FROM Pessoa p, Voto v, MesaDeVoto mv
            WHERE p.id=v.pessoa_id and v.mesa_de_voto_id=mv.id and p.id=%s and mv.eleicao_id=%s;
        '''

        cur.execute(search_statement, (user_id, election_id,))
        users = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return users
