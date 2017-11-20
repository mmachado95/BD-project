import psycopg2


def create_tables():
    # TODO missing votes and results tables
    commands = (
        """
        CREATE TABLE faculdade (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE departamento (
            id SERIAL PRIMARY KEY,
            faculdade_id integer NOT NULL,
            nome VARCHAR(255) NOT NULL,
            FOREIGN KEY (faculdade_id) REFERENCES faculdade (id)
        )
        """,
        """
        CREATE TABLE pessoa (
            id SERIAL PRIMARY KEY,
            departmento_id integer NOT NULL,
            nome VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            contacto VARCHAR(100) NOT NULL,
            morada VARCHAR(100) NOT NULL,
            cc VARCHAR(10) NOT NULL,
            data_validade date NOT NULL,
            tipo smallint NOT NULL,
            FOREIGN KEY (departmento_id) REFERENCES departamento (id)
        )
        """,
        """
        CREATE TABLE eleicao (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao VARCHAR(500) NOT NULL,
            inicio date NOT NULL,
            fim date NOT NULL,
            acabou boolean NOT NULL
        )
        """,
        """
        CREATE TABLE conselho_geral (
            id integer PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES eleicao (id)
        )
        """,
        """
        CREATE TABLE nucleo_de_estudantes (
            id integer PRIMARY KEY,
            departmento_id integer NOT NULL,
            FOREIGN KEY (id) REFERENCES eleicao (id),
            FOREIGN KEY (departmento_id) REFERENCES departamento (id)
        )
        """,
        """
        CREATE TABLE direcao_departamento (
            id integer PRIMARY KEY,
            departmento_id integer NOT NULL,
            FOREIGN KEY (id) REFERENCES eleicao (id),
            FOREIGN KEY (departmento_id) REFERENCES departamento (id)
        )
        """,
        """
        CREATE TABLE direcao_faculdade (
            id integer PRIMARY KEY,
            faculdade_id integer NOT NULL,
            FOREIGN KEY (id) REFERENCES eleicao (id),
            FOREIGN KEY (faculdade_id) REFERENCES faculdade (id)
        )
        """,
        """
        CREATE TABLE lista (
            id integer PRIMARY KEY,
            eleicao_id integer NOT NULL,
            name varchar(100) NOT NULL,
            type smallint NOT NULL,
            FOREIGN KEY (eleicao_id) REFERENCES eleicao (id)
        )
        """,
        """
        CREATE TABLE lista_de_candidato (
            lista_id integer NOT NULL,
            pessoa_id integer NOT NULL,
            FOREIGN KEY (lista_id) REFERENCES lista (id),
            FOREIGN KEY (pessoa_id) REFERENCES pessoa (id)
        )
        """,
        """
        CREATE TABLE mesa_de_voto (
            id SERIAL PRIMARY KEY,
            eleicao_id integer NOT NULL,
            departmento_id integer NOT NULL,
            FOREIGN KEY (eleicao_id) REFERENCES eleicao (id),
            FOREIGN KEY (departmento_id) REFERENCES departamento (id)
        )
        """,
        """
        CREATE TABLE terminais_de_voto (
            id SERIAL PRIMARY KEY,
            mesa_de_voto_id integer NOT NULL,
            FOREIGN KEY (mesa_de_voto_id) REFERENCES mesa_de_voto (id)
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
