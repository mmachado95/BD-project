import psycopg2


"""
Parse sql file for commands to run
"""
def get_commands(filename):
    f = open(filename, 'r')
    commands = f.read()
    return commands.split(';')


"""
Connect to database
"""
def connect_db():
    conn = None
    try:
        conn = psycopg2.connect(host='localhost', dbname='ivotas', user='Machado', password='')
    except(Exception, psycopg2.DatabaseError) as error:
        print('Unable to connect to database %s' % error)
    finally:
        return conn
