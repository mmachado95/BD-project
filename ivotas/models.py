import psycopg2


"""
Parse sql file for commands to run
"""
def get_commands(filename):
    f = open(filename, 'r')
    commands = f.read()
    return commands.split(';')


"""
Create tables at startup
"""
def create_tables():
    commands = get_commands('ivotas/create_tables.sql')

    conn = None
    try:
        conn_params = "host='localhost' dbname='ivotas' user='Machado' password=''"
        conn = psycopg2.connect(conn_params)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            # empty line or comment
            if command.strip() != '' or command[0:2]=='--':
                cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


"""
Seed tables with test values
"""
def seed_tables():
    commands = get_commands('ivotas/seeds.sql')

    conn = None
    try:
        conn_params = "host='localhost' dbname='ivotas' user='Machado' password=''"
        conn = psycopg2.connect(conn_params)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            if command.strip() != '':
                cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


#################################
### Create records functions  ###
#################################

"""
Register new user
"""
def create_user(name, department, password, contact, address, cc, end_date, type):
    conn = None
    try:
        # connect to database and create cursor to execute commands in database session
        conn_params = "host='localhost' dbname='ivotas' user='Machado' password=''"
        conn = psycopg2.connect(conn_params)
        cur = conn.cursor()

        # fetch department_id of user
        cur.execute(
            'SELECT id FROM departamento WHERE nome= %(name)s',
            {'name': department}
        )
        department_id = cur.fetchone()

        # insert user in table
        insert_statement = '''
            INSERT INTO pessoa(departamento_id, nome, password, contacto, morada, cc, data_validade, tipo)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(insert_statement, (department_id, name, password, contact, address, cc, end_date, type,))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
