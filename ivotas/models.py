import psycopg2
from ivotas.utils import get_db, close_db, get_commands, get_search_statement


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
    finally:
        close_db()


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
    finally:
        close_db()


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

        # insert faculty in table
        insert_statement = '''INSERT INTO faculdade(nome) VALUES(%s)'''
        cur.execute(insert_statement, (name,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new department
"""
def create_department(faculty_id, name):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert department in table
        insert_statement = '''
            INSERT INTO departamento(faculdade_id, nome)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (faculty_id, name,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new user
"""
def create_user(department_id, name, password, contact, address, cc, end_date, type):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert user in table
        insert_statement = '''
            INSERT INTO pessoa(departamento_id, nome, password, contacto, morada, cc, data_validade, tipo)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(insert_statement, (department_id, name, password, contact, address, cc, end_date, type,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new election
"""
def create_election(faculty_id, department_id, name, description, start, end, finished, type):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert election in table
        insert_statement = '''
            INSERT INTO eleicao(faculdade_id, departamento_id, nome, descricao, inicio, fim, acabou, tipo)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(insert_statement, (faculty_id, department_id, name, description, start, end, finished, type,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new list for election
"""
def create_list(election_id, name, type, users_ids):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list
        insert_statement = '''
            INSERT INTO lista(eleicao_id, nome, tipo)
            VALUES(%s, %s, %s)
            RETURNING id
        '''
        cur.execute(insert_statement, (election_id, name, type,))

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
    finally:
        close_db()


"""
Create new voting table
"""
def create_voting_table(election_id, department_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert voting table
        insert_statement = '''
            INSERT INTO mesa_de_voto(eleicao_id, departamento_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (election_id, department_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


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
    finally:
        close_db()


"""
Create new vote
"""
def create_vote(user_id, election_id, department_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert vote
        insert_statement = '''
            INSERT INTO voto(pessoa_id, eleicao_id, departamento_id)
            VALUES(%s, %s, %s)
        '''
        cur.execute(insert_statement, (user_id, election_id, department_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new list results
"""
def create_list_results(list_id, number_of_votes, percentage_of_votes):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert list results
        insert_statement = '''
            INSERT INTO resultados_lista(lista_id, numero_votos, percentagem_votos)
            VALUES(%s, %s, %s)
        '''
        cur.execute(insert_statement, (list_id, number_of_votes, percentage_of_votes,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


"""
Create new results
"""
def create_results(election_id, list_results_id):
    try:
        # connect to database and create cursor to execute commands in database session
        cur = get_db('ivotas').cursor()

        # insert results
        insert_statement = '''
            INSERT INTO resultados(eleicao_id, resultados_lista_id)
            VALUES(%s, %s)
        '''
        cur.execute(insert_statement, (election_id, list_results_id,))

        # commit the changes
        get_db('ivotas').commit()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()


########################
### Query functions ###
########################

"""
Search faculties
"""
def search_faculty(**kwargs):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        search_statement = get_search_statement('faculdade', kwargs)
        cur.execute(search_statement)
        faculties = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()
        return faculties


"""
Search department
"""
def search_department(**kwargs):
    try:
        # connect to database
        cur = get_db('ivotas').cursor()

        # get all departments
        search_statement = get_search_statement('departamento', kwargs)
        cur.execute(search_statement)
        departments = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close_db()
        return departments
