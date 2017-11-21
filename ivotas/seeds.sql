INSERT INTO faculdade (nome)
VALUES
  ('FCTUC'),
  ('FEUC');

INSERT INTO departamento (faculdade_id, nome)
VALUES
  ((SELECT id from faculdade WHERE nome='FCTUC'), 'Engenharia Informatica'),
  ((SELECT id from faculdade WHERE nome='FCTUC'), 'Engenharia Mecanica'),
  ((SELECT id from faculdade WHERE nome='FEUC'), 'Economia'),
  ((SELECT id from faculdade WHERE nome='FEUC'), 'Gestao');

INSERT INTO pessoa (departamento_id, nome, password, contacto, morada, cc, data_validade, tipo)
VALUES
  ((SELECT id from departamento WHERE nome='Engenharia Informatica'), 'Teresa', '123', '9140975121', 'RUA A', '11111111', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Engenharia Informatica'), 'Miguel', '123', '9140975122', 'RUA B', '11111112', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Engenharia Mecanica'), 'Pedro', '123', '9140975123', 'RUA C', '11111113', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Engenharia Mecanica'), 'Maria', '123', '9140975124', 'RUA D', '11111114', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Economia'), 'Paula', '123', '9140975125', 'RUA E', '11111115', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Economia'), 'Diogo', '123', '9140975126', 'RUA F', '11111116', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Gestao'), 'Andre', '123', '9140975127', 'RUA G', '11111117', '2017-12-25', 1),
  ((SELECT id from departamento WHERE nome='Gestao'), 'Jose', '123', '9140975128', 'RUA H', '11111118', '2017-12-25', 1);

INSERT INTO eleicao(nome, descricao, inicio, fim, acabou, tipo)
VALUES
  ('NEI', 'Nucleo de estudantes de informatica', '2017-11-20 22:00:00', '2017-12-13 10:15:00', false, 2);

INSERT INTO lista(eleicao_id, nome, tipo)
VALUES
  (1, 'LISTA A', 1),
  (1, 'LISTA B', 1);

INSERT INTO lista_de_candidatos(lista_id, pessoa_id)
VALUES
  (1, 1),
  (1, 3),
  (2, 2);

INSERT INTO mesa_de_voto(eleicao_id, departamento_id)
VALUES
  (1, 1);

INSERT INTO terminal_de_voto(mesa_de_voto_id)
VALUES
  (1),
  (1),
  (1);
