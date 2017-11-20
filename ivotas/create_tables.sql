CREATE TABLE faculdade (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);
CREATE TABLE departamento (
    id SERIAL PRIMARY KEY,
    faculdade_id integer NOT NULL,
    nome VARCHAR(255) NOT NULL,
    FOREIGN KEY (faculdade_id)
        REFERENCES faculdade (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
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
    FOREIGN KEY (departmento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE eleicao (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    inicio date NOT NULL,
    fim date NOT NULL,
    acabou boolean NOT NULL
);
CREATE TABLE conselho_geral (
    id integer PRIMARY KEY,
    FOREIGN KEY (id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE nucleo_de_estudantes (
    id integer PRIMARY KEY,
    departmento_id integer NOT NULL,
    FOREIGN KEY (id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departmento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE direcao_departamento (
    id integer PRIMARY KEY,
    departmento_id integer NOT NULL,
    FOREIGN KEY (id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departmento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE direcao_faculdade (
    id integer PRIMARY KEY,
    faculdade_id integer NOT NULL,
    FOREIGN KEY (id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (faculdade_id)
        REFERENCES faculdade (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE lista (
    id integer PRIMARY KEY,
    eleicao_id integer NOT NULL,
    name varchar(100) NOT NULL,
    type smallint NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE lista_de_candidatos (
    lista_id integer NOT NULL,
    pessoa_id integer NOT NULL,
    FOREIGN KEY (lista_id)
        REFERENCES lista (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (pessoa_id)
        REFERENCES pessoa (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE mesa_de_voto (
    id SERIAL PRIMARY KEY,
    eleicao_id integer NOT NULL,
    departmento_id integer NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departmento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE terminal_de_voto (
    id SERIAL PRIMARY KEY,
    mesa_de_voto_id integer NOT NULL,
    FOREIGN KEY (mesa_de_voto_id)
        REFERENCES mesa_de_voto (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE voto (
    id SERIAL PRIMARY KEY,
    pessoa_id integer NOT NULL,
    eleicao_id integer NOT NULL,
    departamento_id integer NOT NULL,
    FOREIGN KEY (pessoa_id)
        REFERENCES pessoa (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departamento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE resultados_lista (
    id SERIAL PRIMARY KEY,
    lista_id integer NOT NULL,
    numero_votos integer NOT NULL,
    percentagem_votos real NOT NULL,
    FOREIGN KEY (lista_id)
        REFERENCES lista (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE resultados (
    eleicao_id integer NOT NULL,
    resultados_lista_id integer NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (resultados_lista_id)
        REFERENCES resultados_lista (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
