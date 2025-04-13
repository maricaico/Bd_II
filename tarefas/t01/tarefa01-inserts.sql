-- 1. Insere Departamentos (cod_gerente inicialmente NULL)

INSERT INTO departamento (descricao)
VALUES
('Dep. História'),      -- código 1
('Dep. Computação'),    -- código 2
('Dep. Geografia'),     -- código 3
('Dep. Direito'),       -- código 4
('Dep. Matemática');    -- código 5


-- 2. Insere Funcionários Gerentes (cod_depto deve existir em departamento)

INSERT INTO funcionario (nome, sexo, dt_nasc, salario, cod_depto)
VALUES
('Ana', 'F', '1988-05-07', 2500.00, 1),       -- código 1 (gerente História)
('Taciano', 'M', '1980-01-25', 2500.00, 2),   -- código 2 (gerente Computação)
('Luciana', 'F', '1982-08-15', 2700.00, 3),   -- código 3 (gerente Geografia)
('Roberto', 'M', '1977-04-10', 3000.00, 4),   -- código 4 (gerente Direito)
('Juliana', 'F', '1985-02-12', 3100.00, 5);   -- código 5 (gerente Matemática)


-- 3. Atualiza Departamentos com cod_gerente

UPDATE departamento SET cod_gerente = 1 WHERE codigo = 1;
UPDATE departamento SET cod_gerente = 2 WHERE codigo = 2;
UPDATE departamento SET cod_gerente = 3 WHERE codigo = 3;
UPDATE departamento SET cod_gerente = 4 WHERE codigo = 4;
UPDATE departamento SET cod_gerente = 5 WHERE codigo = 5;


-- 4. Insere demais Funcionários (cod_depto pode ser NULL ou existente)

INSERT INTO funcionario (nome, sexo, dt_nasc, salario, cod_depto)
VALUES
('Maria', 'F', '1981-07-01', 2500.00, 1),       
('Josefa', 'F', '1986-09-17', 2500.00, 1),      
('Carlos', 'M', '1985-11-21', 2500.00, 2),      
('José', 'M', '1979-07-12', 3500.00, NULL),     
('Gabriel', 'M', '1981-08-11', 1850.00, 3),     
('Margarete', 'F', '1992-03-22', 4500.00, 3),   
('Xuxa', 'F', '1970-03-28', 13500.00, NULL),    
('Victor', 'M', '1970-03-28', 500.00, 4),       
('Humberto', 'M', '1970-05-07', 1500.00, 2),    
('Doisberto', 'M', '1980-07-14', 2500.00, 3),   
('Tresberta', 'F', '1992-09-01', 3000.00, 5);   


-- 5. Insere Projetos (cod_depto e cod_responsavel devem existir)

INSERT INTO projeto (nome, descricao, cod_depto, cod_responsavel, data_inicio, data_fim)
VALUES
('APF', 'Analisador de Ponto de Função', 2, 2, '2018-02-26', '2019-06-30'),       -- código 1
('Monitoria', 'Projeto de Monitoria 2019.1', 1, 9, '2019-02-26', '2019-12-30'),   -- código 2
('BD', 'Projeto de Banco de Dados', 3, 10, '2018-02-26', '2018-06-30'),           -- código 3
('ES', 'Projeto de Engenharia de Software', 1, 1, '2018-02-26', '2018-06-30'),    -- código 4
('TCC', 'Projeto de Conclusão de Curso', 5, 5, '2020-01-01', '2020-12-01');       -- código 5


-- 6. Insere Atividades (cod_responsavel e projeto devem existir)

INSERT INTO atividade (nome, descricao, cod_responsavel, projeto, data_inicio, data_fim)
VALUES
('APF1', 'APF - Atividade 1', 2, 1, '2018-02-26', '2018-06-30'),
('APF2', 'APF - Atividade 2', 2, 1, '2018-06-26', '2018-07-30'),
('APF3', 'APF - Atividade 3', 9, 1, '2018-08-26', '2018-09-30'),
('APF4', 'APF - Atividade 4', 9, 1, '2018-08-26', '2018-09-30'),
('APF5', 'APF - Atividade 5', 9, 1, '2018-09-30', '2018-10-30'),

('MON1', 'Monitoria - Atividade 1', 6, 2, '2019-03-01', '2019-03-20'),
('MON2', 'Monitoria - Atividade 2', 7, 2, '2019-04-01', '2019-04-25'),

('BD1', 'BD - Atividade 1', 10, 3, '2018-06-26', '2018-07-30'),
('BD2', 'BD - Atividade 2', 10, 3, '2018-08-26', '2018-09-30'),
('BD3', 'BD - Atividade 3', 11, 3, '2018-08-26', '2018-09-30'),

('ES1', 'ES - Atividade 1', 1, 4, '2018-09-30', '2018-10-30'),
('ES2', 'ES - Atividade 2', 1, 4, '2018-06-26', '2018-07-30'),

('TCC1', 'TCC - Atividade 1', 5, 5, '2020-02-01', '2020-03-01'),
('TCC2', 'TCC - Atividade 2', 5, 5, '2020-04-01', '2020-05-01');


-- 7. Relaciona atividades aos projetos

INSERT INTO atividade_projeto (cod_projeto, cod_atividade)
VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),

(2, 6),
(2, 7),

(3, 8),
(3, 9),
(3, 10),

(4, 11),
(4, 12),

(5, 13),
(5, 14);
