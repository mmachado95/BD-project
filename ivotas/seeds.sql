INSERT INTO UnidadeOrganica (nome)
VALUES
('FCTUC'),
('FEUC'),
('Engenharia Informatica'),
('Engenharia Mecanica'),
('Economia'),
('Gestao');

INSERT INTO Faculdade (unidade_organica_id)
VALUES
(1),
(2);

INSERT INTO Departamento (unidade_organica_id, faculdade_id)
VALUES
(3, 1),
(4, 1),
(5, 2),
(6, 2);

INSERT INTO Pessoa (unidade_organica_id, nome, password, contacto, morada, cc, data_validade, tipo)
VALUES
  (3, 'Teresa', '123', '9140975121', 'RUA A', '11111111', '2017-12-25', 3),
  (3, 'Miguel', '123', '9140975122', 'RUA B', '11111112', '2017-12-25', 3),
  (4, 'Pedro', '123', '9140975123', 'RUA C', '11111113', '2017-12-25', 3),
  (4, 'Maria', '123', '9140975124', 'RUA D', '11111114', '2017-12-25', 3),
  (5, 'Paula', '123', '9140975125', 'RUA E', '11111115', '2017-12-25', 3),
  (5, 'Diogo', '123', '9140975126', 'RUA F', '11111116', '2017-12-25', 3),
  (6, 'Andre', '123', '9140975127', 'RUA G', '11111117', '2017-12-25', 3),
  (6, 'Jose', '123', '9140975128', 'RUA H', '11111118', '2017-12-25', 3),
  (3, 'David', '123', '9140975129', 'RUA I', '11111119', '2017-12-25', 1),
  (3, 'Rafael', '123', '9140975130', 'RUA J', '11111120', '2017-12-25', 1),
  (4, 'Rafaela', '123', '9140975131', 'RUA K', '11111121', '2017-12-25', 1),
  (4, 'Joana', '123', '9140975132', 'RUA L', '11111122', '2017-12-25', 1),
  (5, 'Ana', '123', '9140975133', 'RUA M', '11111123', '2017-12-25', 2),
  (5, 'Luisa', '123', '9140975134', 'RUA N', '11111124', '2017-12-25', 2),
  (6, 'Tiago', '123', '9140975135', 'RUA O', '11111125', '2017-12-25', 2),
  (6, 'Antonio', '123', '9140975136', 'RUA P', '11111126', '2017-12-25', 2);

INSERT INTO Pessoa (unidade_organica_id, nome, password, contacto, morada, cc, data_validade, tipo, administrador)
VALUES
  (1, 'admin', 'admin', '91409753', 'RUA', '11111127', '2017-12-25', 2, TRUE);

INSERT INTO Eleicao(nome, descricao, inicio, fim, tipo)
VALUES
  ('CG 2', 'Conselho Geral 2', '2017-11-20 22:00:00', '2017-12-22 10:15:00', 1), --> id: 1
  ('CG 3', 'Conselho Geral 3', '2017-12-20 22:00:00', '2017-12-21 10:15:00', 1); --> id: 2

INSERT INTO Eleicao(nome, descricao, inicio, fim, tipo, total_votos, votos_brancos, votos_nulos)
VALUES
  ('CG 1', 'Conselho Geral', '2017-11-20 22:00:00', '2017-11-13 10:15:00', 1, 6, 1, 1); --> id: 3 PASSADA

INSERT INTO Eleicao(nome, unidade_organica_id, descricao, inicio, fim, tipo)
VALUES
  ('NEI', 3, 'Nucleo de Estudantes de Informatica', '2017-11-20 22:00:00', '2017-12-22 10:15:00', 2), --> id: 4
  ('NEG', 6, 'Nucleo de Estudantes de Gestao', '2017-12-20 22:00:00', '2017-12-21 10:15:00', 2); --> id: 5

INSERT INTO Eleicao(nome, unidade_organica_id, descricao, inicio, fim, tipo, total_votos, votos_brancos, votos_nulos)
VALUES
  ('NEM', 4, 'Nucleo de Estudantes de Mecanica', '2017-11-20 22:00:00', '2017-11-13 10:15:00', 2, 4, 2, 1); --> id: 6 PASSADA

INSERT INTO Lista(eleicao_id, nome, numero_votos)
VALUES
  (6, 'LISTA NEM A', 1), --> 1 voto
  (6, 'LISTA NEM B', 0), --> 1 voto
  (3, 'LISTA CG1 ALUNOS C', 0), --> 0 votos
  (3, 'LISTA CG1 ALUNOS D', 2), --> 2 votos
  (3, 'LISTA CG1 DOCENTES A', 0), --> 0 votos
  (3, 'LISTA CG1 DOCENTES B', 1), --> 1 voto
  (3, 'LISTA CG1 FUNCIONARIOS X', 0), --> 0 voto
  (3, 'LISTA CG1 FUNCIONARIOS Z', 1); --> 1 voto

INSERT INTO Lista(eleicao_id, nome)
VALUES
  (4, 'LISTA NEI E'),
  (4, 'LISTA NEI F'),
  (1, 'LISTA CG2 G'),
  (1, 'LISTA CG2 H'),
  (5, 'LISTA NEG I'),
  (5, 'LISTA NEG J'),
  (2, 'LISTA CG3 K'),
  (2, 'LISTA CG3 L');

INSERT INTO ListaDeCandidatos(lista_id, pessoa_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 9),
  (6, 10),
  (7, 14),
  (8, 15);

INSERT INTO MesaDeVoto(eleicao_id, unidade_organica_id)
VALUES
  (6, 1),
  (3, 1);

INSERT INTO TerminalDeVoto(mesa_de_voto_id)
VALUES
  (1),
  (2),
  (2);

-- 1 ao 8 9 ao 12 13 ao 16
INSERT INTO Voto(pessoa_id, mesa_de_voto_id, momento)
VALUES
  (3, 1, '2017-11-20 22:00:03'), -- aluno a votar em branco
  (4, 1, '2017-11-20 22:00:04'), -- aluno a votar em nulo
  (3, 1, '2017-11-20 22:00:03'), -- aluno a votar em branco
  (4, 1, '2017-11-20 22:00:04'), -- aluno a votar em nulo
  (10, 2, '2017-11-20 22:00:04'), -- docente a votar em lista
  (14, 2, '2017-11-20 22:00:04'), -- funcionario a votar em lista
  (5, 2, '2017-11-20 22:00:04'), -- aluno a votar em lista
  (6, 2, '2017-11-20 22:00:04'), -- aluno a votar em lista
  (12, 2, '2017-11-20 22:00:04'), -- random branco
  (13, 2, '2017-11-20 22:00:04');
