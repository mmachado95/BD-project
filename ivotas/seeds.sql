INSERT INTO unidade_organica (nome)
VALUES
('FCTUC'),
('FEUC'),
('Engenharia Informatica'),
('Engenharia Mecanica'),
('Economia'),
('Gestao');

INSERT INTO faculdade (unidade_organica_id)
VALUES
(1),
(2);

INSERT INTO departamento (unidade_organica_id, faculdade_id)
VALUES
(3, 1),
(4, 1),
(5, 2),
(6, 2);

INSERT INTO pessoa (unidade_organica_id, nome, password, contacto, morada, cc, data_validade, tipo)
VALUES
  (3, 'Teresa', '123', '9140975121', 'RUA A', '11111111', '2017-12-25', 1),
  (3, 'Miguel', '123', '9140975122', 'RUA B', '11111112', '2017-12-25', 1),
  (4, 'Pedro', '123', '9140975123', 'RUA C', '11111113', '2017-12-25', 1),
  (4, 'Maria', '123', '9140975124', 'RUA D', '11111114', '2017-12-25', 1),
  (5, 'Paula', '123', '9140975125', 'RUA E', '11111115', '2017-12-25', 1),
  (5, 'Diogo', '123', '9140975126', 'RUA F', '11111116', '2017-12-25', 1),
  (6, 'Andre', '123', '9140975127', 'RUA G', '11111117', '2017-12-25', 1),
  (6, 'Jose', '123', '9140975128', 'RUA H', '11111118', '2017-12-25', 1);

INSERT INTO eleicao(nome, descricao, inicio, fim, acabou, tipo)
VALUES
  ('NEI', 'Nucleo de estudantes de informatica', '2017-11-20 22:00:00', '2017-12-13 10:15:00', false, 2);

INSERT INTO lista(eleicao_id, nome)
VALUES
  (1, 'LISTA A'),
  (1, 'LISTA B');

INSERT INTO lista_de_candidatos(lista_id, pessoa_id)
VALUES
  (1, 1),
  (1, 3),
  (2, 2);

INSERT INTO mesa_de_voto(eleicao_id, unidade_organica_id)
VALUES
  (1, 1);

INSERT INTO terminal_de_voto(mesa_de_voto_id)
VALUES
  (1),
  (1),
  (1);
