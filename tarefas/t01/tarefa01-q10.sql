 SELECT
    p.nome AS nome_projeto,
    d_proj.descricao AS nome_departamento_projeto,
    f_resp.nome AS nome_funcionario_responsavel,
    d_func.descricao AS nome_departamento_funcionario
FROM
    projeto p
LEFT JOIN 
    departamento d_proj ON p.cod_depto = d_proj.codigo
LEFT JOIN 
    funcionario f_resp ON p.cod_responsavel = f_resp.codigo
LEFT JOIN 
    departamento d_func ON f_resp.cod_depto = d_func.codigo
ORDER BY
    nome_projeto; 