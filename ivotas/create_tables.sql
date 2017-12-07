-- Delete old tables if they exist
DROP TABLE IF EXISTS voto;
DROP TABLE IF EXISTS terminal_de_voto;
DROP TABLE IF EXISTS mesa_de_voto;
DROP TABLE IF EXISTS lista_de_candidatos;
DROP TABLE IF EXISTS lista;
DROP TABLE IF EXISTS eleicao;
DROP TABLE IF EXISTS pessoa;
DROP TABLE IF EXISTS departamento;
DROP TABLE IF EXISTS faculdade;
DROP TABLE IF EXISTS unidade_organica;


CREATE TABLE unidade_organica (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
CREATE TABLE faculdade (
    unidade_organica_id integer NOT NULL,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES unidade_organica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE departamento (
    unidade_organica_id integer NOT NULL,
    faculdade_id integer NOT NULL,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES unidade_organica (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (faculdade_id)
    REFERENCES unidade_organica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- 1 - professor
-- 2 - funcionario
-- 3 - aluno
CREATE TABLE pessoa (
    id SERIAL PRIMARY KEY,
    unidade_organica_id integer NOT NULL,
    nome VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    morada VARCHAR(100) NOT NULL,
    cc VARCHAR(10) NOT NULL UNIQUE,
    data_validade date NOT NULL,
    tipo smallint NOT NULL,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES unidade_organica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- 1- conselho geral
-- 2- nucleo estudantes
-- 3- dir faculdade
-- 4- dir dep
CREATE TABLE eleicao (
    id SERIAL PRIMARY KEY,
    unidade_organica_id integer,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    inicio timestamp NOT NULL,
    fim timestamp NOT NULL,
    tipo smallint NOT NULL,
    total_votos integer DEFAULT 0,
    votos_brancos integer DEFAULT 0,
    percentagem_brancos real DEFAULT 0.0,
    votos_nulos integer DEFAULT 0,
    percentagem_nulos real DEFAULT 0.0,
    FOREIGN KEY (unidade_organica_id)
      REFERENCES unidade_organica (id)
      ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE lista (
    id SERIAL PRIMARY KEY,
    eleicao_id integer NOT NULL,
    nome varchar(100) NOT NULL,
    numero_votos integer DEFAULT 0,
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
    unidade_organica_id integer NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES unidade_organica (id)
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
    mesa_de_voto_id integer NOT NULL,
    FOREIGN KEY (pessoa_id)
        REFERENCES pessoa (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (mesa_de_voto_id)
        REFERENCES mesa_de_voto (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
