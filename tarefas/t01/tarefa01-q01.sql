SELECT f.nome
FROM funcionario f
WHERE f.salario > ALL (
    SELECT salario
    FROM funcionario
    WHERE cod_depto = 2
);
  