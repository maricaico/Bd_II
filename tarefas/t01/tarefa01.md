[scripts-create](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-create.sql)

[scripts-insert](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-inserts.ql)

[questão 01](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-q01.sql)

[questão 04](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-q04.sql)

[questão 07](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-q07.sql)

[questão 10](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-q10.sql)

[questão 13](https://github.com/maricaico/Bd_II/blob/main/tarefas/t01/tarefa01-q13.sql)



## CROSS JOIN e NATURAL JOIN no SQL

### CROSS JOIN

O `CROSS JOIN` realiza uma junção cruzada entre duas tabelas, gerando o produto cartesiano. Isso significa que cada linha da primeira tabela será combinada com todas as linhas da segunda tabela. O número total de linhas no resultado será o número de linhas da primeira tabela multiplicado pelo número de linhas da segunda.

Esse tipo de junção é útil quando se deseja obter todas as combinações possíveis entre dois conjuntos de dados. No entanto, também pode surgir por engano, especialmente quando se usa a sintaxe de vírgula entre tabelas e se esquece de colocar uma condição de junção.

**Sintaxe:**

```sql
SELECT * 
FROM tabela1 
CROSS JOIN tabela2;

```
#### Exemplo

Considere a tabela Cores com os valores vermelho e azul, e a tabela Tamanhos com os valores P e M. A consulta:

```sql
SELECT * FROM Cores CROSS JOIN Tamanhos;

```
#### Tabela

| Cores  | Tamanhos |
| ------------- |:-------------:|
| vermelho     | P    |
| vermelho      | M    |
| azul      | P    |
| azul      | M    |

Nesse exemplo, o resultado mostra todas as possíveis combinações entre as cores e os tamanhos disponíveis. É exatamente para esse tipo de situação que o CROSS JOIN é útil.


### NATURAL JOIN

O NATURAL JOIN realiza uma junção automática entre duas tabelas, utilizando como critério todas as colunas que possuam exatamente o mesmo nome em ambas. Ele compara os valores dessas colunas e retorna apenas as linhas onde os valores coincidem. No resultado final, as colunas em comum aparecem apenas uma vez.

Apesar de parecer prático, o NATURAL JOIN pode ser perigoso em ambientes de produção. Isso porque ele depende da existência de colunas com o mesmo nome, e qualquer mudança na estrutura das tabelas (como a adição ou renomeação de colunas) pode alterar o comportamento da consulta sem gerar erro, o que dificulta a manutenção e pode gerar resultados incorretos.

**Sintaxe:**

```sql
SELECT * 
FROM tabela1 
CROSS JOIN tabela2;

```
#### Exemplo

Suponha a tabela Pedidos com as colunas id_cliente e produto, e a tabela Clientes com as colunas id_cliente e nome_cliente. A consulta:

```sql
SELECT * FROM Pedidos NATURAL JOIN Clientes;

```
#### Tabela

| Id_cliente  | Produto | Nome_cliente |
| ------------- |:-------------:|:-------------:|
| 1    | Tênis    |azul      | Ana    |
| 2      | Camiseta    | azul      | João   |

Esse join funciona corretamente porque id_cliente é a única coluna com o mesmo nome nas duas tabelas. No entanto, se ambas também tivessem uma coluna chamada data_modificacao, o NATURAL JOIN tentaria unir por id_cliente e por data_modificacao, o que provavelmente não é o comportamento desejado.




