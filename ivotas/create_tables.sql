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
    departamento_id integer NOT NULL,
    nome VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    morada VARCHAR(100) NOT NULL,
    cc VARCHAR(10) NOT NULL UNIQUE,
    data_validade date NOT NULL,
    tipo smallint NOT NULL,
    FOREIGN KEY (departamento_id)
        REFERENCES departamento (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- 1- conselho geral
-- 2- nucleo estudantes
-- 3- dir faculdade
-- 4- dir dep
CREATE TABLE eleicao (
    id SERIAL PRIMARY KEY,
    faculdade_id integer,
    departamento_id integer,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    inicio timestamp NOT NULL,
    fim timestamp NOT NULL,
    acabou boolean NOT NULL,
    tipo smallint NOT NULL,
    votos_brancos integer DEFAULT 0,
    percentagem_brancos real DEFAULT 0.0,
    votos_nulos integer DEFAULT 0,
    percentagem_nulos real DEFAULT 0.0,
    FOREIGN KEY (faculdade_id)
      REFERENCES faculdade (id)
      ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departamento_id)
      REFERENCES departamento (id)
      ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE lista (
    id integer PRIMARY KEY,
    eleicao_id integer NOT NULL,
    nome varchar(100) NOT NULL,
    tipo smallint NOT NULL,
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
    departamento_id integer NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (departamento_id)
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
