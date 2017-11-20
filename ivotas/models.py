import psycopg2


def get_commands(filename):
    f = open(filename, 'r')
    commands = f.read()
    return commands.split(';')


def create_tables():
    commands = get_commands('ivotas/create_tables.sql')

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
