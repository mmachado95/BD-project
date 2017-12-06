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

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


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

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


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
        insert_statement = '''INSERT INTO unidade_organica(nome) VALUES(%s) RETURNING id'''
        cur.execute(insert_statement, (name,))
        organic_unit_id = cur.fetchone()[0]

        # insert faculty in table
        insert_statement = '''INSERT INTO faculdade(unidade_organica_id) VALUES(%s)'''
        cur.execute(insert_statement, (organic_unit_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new department
"""
def create_department(name, faculty_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # create organic_unit
        insert_statement = '''INSERT INTO unidade_organica(nome) VALUES(%s) RETURNING id'''
        cur.execute(insert_statement, (name,))
        organic_unit_id = cur.fetchone()[0]

        # insert department in table
        insert_statement = '''
            INSERT INTO departamento(unidade_organica_id, faculdade_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (organic_unit_id, faculty_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new user
"""
def create_user(organic_unit_id, name, password, contact, address, cc, end_date, type):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert user in table
        insert_statement = '''
            INSERT INTO pessoa(unidade_organica_id, nome, password, contacto, morada, cc, data_validade, tipo)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(insert_statement, (organic_unit_id, name, password, contact, address, cc, end_date, type,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


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
                INSERT INTO eleicao(unidade_organica_id, nome, descricao, inicio, fim, tipo)
                VALUES(%s, %s, %s, %s, %s, %s)
            '''
            cur.execute(insert_statement, (organic_unit, name, description, start, finished, type,))
        else:
            insert_statement = '''
                INSERT INTO eleicao(nome, descricao, inicio, fim, tipo)
                VALUES(%s, %s, %s, %s, %s)
            '''
            cur.execute(insert_statement, (name, description, start, finished, type,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new list for election
"""
def create_list(election_id, name, users_ids):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list
        insert_statement = '''
            INSERT INTO lista(eleicao_id, nome)
            VALUES(%s, %s)
            RETURNING id
        '''
        cur.execute(insert_statement, (election_id, name,))

        # get list id and create new insert statement
        list_id = cur.fetchone()[0]
        insert_statement = '''
            INSERT INTO lista_de_candidatos(lista_id, pessoa_id)
            VALUES(%s, %s)
        '''

        # add users to list
        for user_id in users_ids:
            cur.execute(insert_statement, (list_id, user_id))
        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def add_candidates(list_id, users_ids):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list
        insert_statement = '''
            INSERT INTO lista_de_candidatos(lista_id, pessoa_id)
            VALUES(%s, %s)
        '''

        # add users to list
        for user_id in users_ids:
            cur.execute(insert_statement, (str(list_id), str(user_id)))
        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new voting table
"""
def create_voting_table(election_id, organic_unit_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert voting table
        insert_statement = '''
            INSERT INTO mesa_de_voto(eleicao_id, unidade_organica_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (election_id, organic_unit_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new voting terminal
"""
def create_voting_terminal(voting_table_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert voting terminal
        insert_statement = '''
            INSERT INTO terminal_de_voto(mesa_de_voto_id)
            VALUES(%s)
        '''
        cur.execute(insert_statement, (voting_table_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Create new vote
"""
def create_vote(user_id, voting_table_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert vote
        insert_statement = '''
            INSERT INTO voto(pessoa_id, mesa_de_voto_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (user_id, voting_table_id))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


########################
### Query functions ###
########################


"""
Get organic units
"""
def get_organic_units(type):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get organic units
        if type is not None and type != 2:
            if type == 3:
                search_statement = '''
                    SELECT id, nome
                    FROM unidade_organica, faculdade
                    WHERE id=unidade_organica_id
                '''
            elif type == 4:
                search_statement = '''
                    SELECT id, nome
                    FROM unidade_organica, departamento
                    WHERE id=unidade_organica_id
                '''
        else:
            search_statement = '''
                SELECT id, nome
                FROM unidade_organica
            '''

        cur.execute(search_statement)
        organic_units = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
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
            FROM unidade_organica, faculdade
            WHERE id=unidade_organica_id
        '''
        cur.execute(search_statement)
        faculties = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return faculties


"""
Get departments
"""
def get_departments():
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get departments
        search_statement = '''
            SELECT id, nome
            FROM unidade_organica, departamento
            WHERE id=unidade_organica_id
        '''
        cur.execute(search_statement)
        departments = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return departments


"""
Get elections
"""
def get_elections(form_friendly, not_happening):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get elections
        if form_friendly:
            search_statement = '''
                SELECT id, nome
                FROM eleicao
            '''
            cur.execute(search_statement)
        elif not_happening:
            now = datetime.datetime.now()
            search_statement = '''
                SELECT id, nome
                FROM eleicao
                where inicio > timestamp %s;
            '''
            cur.execute(search_statement, (now,))
        else:
            search_statement = '''
                SELECT *
                FROM eleicao

            '''
            cur.execute(search_statement)

        elections = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return elections


"""
Get voting tables
"""
def get_voting_tables(form_friendly):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get voting talbles
        if form_friendly:
            search_statement = '''
                SELECT mv.id, e.nome || ' ' || uo.nome
                FROM mesa_de_voto mv, eleicao e, unidade_organica uo
                WHERE mv.eleicao_id=e.id and mv.unidade_organica_id=uo.id
            '''
        else:
            search_statement = '''
                SELECT *
                FROM eleicao
            '''
        cur.execute(search_statement)
        elections = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
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
                FROM lista
            '''
        else:
            search_statement = '''
                SELECT *
                FROM lista
            '''
        cur.execute(search_statement)
        lists = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return lists


"""
Get users
"""
def get_users(form_friendly):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get users
        if form_friendly:
            search_statement = '''
                SELECT id, 'Nome: ' || nome || ' ' || 'CC: ' || cc "Identificador"
                FROM pessoa
            '''
        else:
            search_statement = '''
                SELECT *
                FROM pessoa
            '''
        cur.execute(search_statement)
        users = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return users


"""
Get users
"""
def get_list_of_candidates(add_candidates, remove_candidates):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # TODO this fix optimizes the fix that is in the functions at the app
        # get users
        if add_candidates['status']:
            search_statement = '''
                SELECT id
                FROM pessoa
                EXCEPT
                SELECT pessoa_id
                FROM lista_de_candidatos
                WHERE lista_id=%s
            '''
            list_id = add_candidates['list_id']
            cur.execute(search_statement, (list_id,))
        elif remove_candidates['status']:
            search_statement = '''
                SELECT pessoa_id
                FROM lista_de_candidatos
                WHERE lista_id = %s
            '''
            list_id = remove_candidates['list_id']
            cur.execute(search_statement, (list_id,))
        else:
            search_statement = '''
                SELECT *
                FROM lista_de_candidatos
            '''
            cur.execute(search_statement)
        candidates = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
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
            FROM unidade_organica
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
            FROM unidade_organica, departamento
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
                FROM mesa_de_voto mv, eleicao e, unidade_organica uo
                WHERE mv.eleicao_id=e.id and mv.unidade_organica_id=uo.id and mv.id=%s
            '''
        elif election_date:
            search_statement = '''
                SELECT inicio, fim
                FROM mesa_de_voto mv, eleicao e
                WHERE mv.eleicao_id=e.id and e.id=%s
            '''
        else:
            search_statement = '''
                SELECT eleicao_id, unidade_organica_id
                FROM mesa_de_voto
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
def search_election(election_id):
    election_id = str(election_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT nome, descricao, inicio, fim, tipo
            FROM eleicao
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
            SELECT id, eleicao_id, nome
            FROM lista
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
Search person by id
"""
def search_user(user_id):
    user_id = str(user_id)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = '''
            SELECT id, nome
            FROM pessoa
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
        update_statement = get_update_statement('unidade_organica', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Update Department
"""
def update_department(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update faculty
        update_statement = get_update_statement('departamento', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Update user
"""
def update_user(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update user
        update_statement = get_update_statement('pessoa', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Update election
"""
def update_election(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update election
        update_statement = get_update_statement('eleicao', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Update list
"""
def update_list(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update list
        update_statement = get_update_statement('lista', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Update voting table
"""
def update_voting_table(id_to_update, **kwargs):
    id_to_update = str(id_to_update)
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # update voting table
        update_statement = get_update_statement('mesa_de_voto', id_to_update, kwargs)
        cur.execute(update_statement)

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


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
        if table == 'lista_de_candidatos':
            delete_statement = 'DELETE FROM ' + table + ' WHERE pessoa_id=%s'
        else:
            delete_statement = 'DELETE FROM ' + table + ' WHERE id=%s'
        cur.execute(delete_statement, (id_to_delete,))

        # commit change
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
