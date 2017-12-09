-- Delete old tables if they exist
DROP TABLE IF EXISTS Voto;
DROP TABLE IF EXISTS TerminalDeVoto;
DROP TABLE IF EXISTS MesaDeVoto;
DROP TABLE IF EXISTS ListaDeCandidatos;
DROP TABLE IF EXISTS Lista;
DROP TABLE IF EXISTS Eleicao;
DROP TABLE IF EXISTS Pessoa;
DROP TABLE IF EXISTS Departamento;
DROP TABLE IF EXISTS Faculdade;
DROP TABLE IF EXISTS UnidadeOrganica;


CREATE TABLE UnidadeOrganica (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);
CREATE TABLE Faculdade (
    unidade_organica_id integer NOT NULL,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES UnidadeOrganica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE Departamento (
    unidade_organica_id integer NOT NULL,
    faculdade_id integer NOT NULL,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES UnidadeOrganica (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (faculdade_id)
    REFERENCES UnidadeOrganica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- 1 - professor
-- 2 - funcionario
-- 3 - aluno
CREATE TABLE Pessoa (
    id SERIAL PRIMARY KEY,
    unidade_organica_id integer NOT NULL,
    nome VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    morada VARCHAR(100) NOT NULL,
    cc VARCHAR(10) NOT NULL UNIQUE,
    data_validade date NOT NULL,
    tipo smallint NOT NULL,
    administrador boolean DEFAULT FALSE,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES UnidadeOrganica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- 1- conselho geral
-- 2- nucleo estudantes
-- 3- dir faculdade
-- 4- dir dep
CREATE TABLE Eleicao (
    id SERIAL PRIMARY KEY,
    unidade_organica_id integer,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    inicio timestamp NOT NULL,
    fim timestamp NOT NULL,
    tipo smallint NOT NULL,
    total_votos integer DEFAULT 0,
    votos_brancos integer DEFAULT 0,
    votos_nulos integer DEFAULT 0,
    FOREIGN KEY (unidade_organica_id)
      REFERENCES UnidadeOrganica (id)
      ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE Lista (
    id SERIAL PRIMARY KEY,
    eleicao_id integer NOT NULL,
    nome varchar(100) NOT NULL,
    numero_votos integer DEFAULT 0,
    FOREIGN KEY (eleicao_id)
        REFERENCES Eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE ListaDeCandidatos (
    lista_id integer NOT NULL,
    pessoa_id integer NOT NULL,
    FOREIGN KEY (lista_id)
        REFERENCES Lista (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (pessoa_id)
        REFERENCES Pessoa (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE MesaDeVoto (
    id SERIAL PRIMARY KEY,
    eleicao_id integer NOT NULL,
    unidade_organica_id integer NOT NULL,
    FOREIGN KEY (eleicao_id)
        REFERENCES Eleicao (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (unidade_organica_id)
        REFERENCES UnidadeOrganica (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE TerminalDeVoto (
    id SERIAL PRIMARY KEY,
    mesa_de_voto_id integer NOT NULL,
    FOREIGN KEY (mesa_de_voto_id)
        REFERENCES MesaDeVoto (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE Voto (
    id SERIAL PRIMARY KEY,
    pessoa_id integer NOT NULL,
    mesa_de_voto_id integer NOT NULL,
    momento timestamp NOT NULL,
    FOREIGN KEY (pessoa_id)
        REFERENCES Pessoa (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (mesa_de_voto_id)
        REFERENCES MesaDeVoto (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
