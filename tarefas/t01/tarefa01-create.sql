DROP TABLE IF EXISTS atividade_projeto CASCADE;
DROP TABLE IF EXISTS atividade CASCADE;
DROP TABLE IF EXISTS projeto CASCADE;
DROP TABLE IF EXISTS departamento CASCADE;
DROP TABLE IF EXISTS funcionario CASCADE;

-- Criação das tabelas 
CREATE TABLE departamento (
    codigo serial PRIMARY KEY,
    descricao varchar(250),
    cod_gerente int  -- FK será adicionada depois
);

CREATE TABLE funcionario (
    codigo serial PRIMARY KEY,
    nome varchar(150),
    sexo char(1),
    dt_nasc date,
    salario numeric(10,2), 
    cod_depto int,
    FOREIGN KEY (cod_depto) REFERENCES departamento(codigo) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Adiciona a FK de gerente no departamento
ALTER TABLE departamento
ADD CONSTRAINT fk_gerente FOREIGN KEY (cod_gerente) REFERENCES funcionario(codigo) ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE projeto (
    codigo serial PRIMARY KEY,
    nome varchar(50) UNIQUE,
    descricao varchar(250),
    cod_responsavel int,
    cod_depto int,
    data_inicio date,
    data_fim date,
    FOREIGN KEY (cod_responsavel) REFERENCES funcionario(codigo) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (cod_depto) REFERENCES departamento(codigo) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE atividade (
    codigo serial PRIMARY KEY,
    nome varchar(50) UNIQUE,
    descricao varchar(250),
    cod_responsavel int,
    projeto int,
    data_inicio date,
    data_fim date,
    FOREIGN KEY (cod_responsavel) REFERENCES funcionario(codigo) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE atividade_projeto (
    cod_projeto int,
    cod_atividade int,
    PRIMARY KEY (cod_projeto, cod_atividade),  
    FOREIGN KEY (cod_projeto) REFERENCES projeto(codigo) ON DELETE CASCADE ON UPDATE CASCADE,  
    FOREIGN KEY (cod_atividade) REFERENCES atividade(codigo) ON DELETE CASCADE ON UPDATE CASCADE   
);