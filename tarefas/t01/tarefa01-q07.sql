CREATE OR REPLACE VIEW funcionarios_por_depto AS
SELECT cod_depto, COUNT(*) AS num_funcionarios
FROM funcionario
WHERE cod_depto IS NOT NULL 
GROUP BY cod_depto; 

SELECT d.descricao AS nome_departamento,
    f_gerente.nome AS nome_gerente,
    COALESCE(vw.num_funcionarios, 0) AS quantidade_funcionarios
FROM departamento d
LEFT JOIN funcionario f_gerente ON d.cod_gerente = f_gerente.codigo 
LEFT JOIN funcionarios_por_depto vw ON d.codigo = vw.cod_depto 
ORDER BY
    d.codigo;