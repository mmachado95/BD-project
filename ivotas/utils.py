import psycopg2
from flask import g


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
    return conn


"""
Safe get  connection to dabase
"""
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


"""
Safe close database connection
"""
def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close
