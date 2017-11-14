import psycopg2


def create_tables():
    # TODO missing votes and results tables
    commands = (
        """
        CREATE TABLE faculties (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE departments (
            id SERIAL PRIMARY KEY,
            faculty_id integer,
            name VARCHAR(255) NOT NULL,
            FOREIGN KEY (faculty_id) REFERENCES faculties (id)
        )
        """,
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            department_id integer,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            contact VARCHAR(100) NOT NULL,
            address VARCHAR(100) NOT NULL,
            cc VARCHAR(10) NOT NULL,
            expire_date date NOT NULL,
            type smallint NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
        """,
        """
        CREATE TABLE elections (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(500) NOT NULL,
            start_date date NOT NULL,
            end_date date NOT NULL,
            finished boolean NOT NULL
        )
        """,
        """
        CREATE TABLE conselho_geral (
            id integer PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES elections (id)
        )
        """,
        """
        CREATE TABLE nucleo_de_estudantes (
            id integer PRIMARY KEY,
            department_id integer,
            FOREIGN KEY (id) REFERENCES elections (id),
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
        """,
        """
        CREATE TABLE direcao_departamento (
            id integer PRIMARY KEY,
            department_id integer,
            FOREIGN KEY (id) REFERENCES elections (id),
        FOREIGN KEY (department_id) REFERENCES departments (id)
        )
        """,
        """
        CREATE TABLE direcao_faculdade (
            id integer PRIMARY KEY,
            faculty_id integer,
            FOREIGN KEY (id) REFERENCES elections (id),
            FOREIGN KEY (faculty_id) REFERENCES faculties (id)
        )
        """,
        """
        CREATE TABLE lists (
            id integer PRIMARY KEY,
            election_id integer,
            name varchar(100) NOT NULL,
            type smallint NOT NULL,
            FOREIGN KEY (id) REFERENCES elections (id)
        )
        """,
        """
        CREATE TABLE candidates_lists (
            list_id integer,
            user_id integer,
            FOREIGN KEY (list_id) REFERENCES lists (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE voting_tables (
            id SERIAL PRIMARY KEY,
            election_id integer,
            department_id integer,
            FOREIGN KEY (election_id) REFERENCES elections (id),
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
        """,
        """
        CREATE TABLE voting_terminal (
            id SERIAL PRIMARY KEY,
            voting_table_id integer,
            FOREIGN KEY (voting_table_id) REFERENCES voting_tables (id)
        )
        """,
    )

    conn = None
    try:
        conn_params = "host='localhost' dbname='ivotas' user='Machado' password=''"
        conn = psycopg2.connect(conn_params)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
