## Links para Scripts e Programas

* [Script de Criação do Esquema e Povoamento Inicial (PostgreSQL)](./scripts_db/schema_e_dados_atividadesbd.sql)


# Tarefa – ODBC e ORM em Python

## ODBC em Python

ODBC (Open Database Connectivity) é uma API padrão desenvolvida pela Microsoft para acessar Sistemas de Gerenciamento de Banco de Dados (SGBDs). Ela permite que aplicações acessem dados de diferentes SGBDs usando uma interface comum, sem precisar se preocupar com as especificidades de cada banco.

Em Python, a principal biblioteca para interagir com bancos de dados via ODBC é a `pyodbc`. Para utilizá-la, são necessários alguns componentes:

1.  **Driver ODBC:** Um software específico para o SGBD que você deseja acessar (ex: PostgreSQL ODBC Driver, SQL Server Native Client, MySQL ODBC Driver). Este driver deve estar instalado no sistema operacional onde o código Python será executado.
2.  **String de Conexão ou DSN:**
    * **String de Conexão:** Fornece diretamente ao `pyodbc` todos os parâmetros necessários para a conexão (nome do driver, servidor, banco de dados, usuário, senha, etc.). É a forma mais comum e flexível em scripts.
    * **DSN (Data Source Name):** Um nome configurado no administrador ODBC do sistema operacional que encapsula os detalhes da conexão. O código Python pode então referenciar apenas o DSN.

**Funcionamento Básico com `pyodbc`:**

* **Conexão:** `conn = pyodbc.connect("DRIVER={PostgreSQL Unicode};SERVER=localhost;DATABASE=atividade_db;UID=usuario;PWD=senha;")` (exemplo para PostgreSQL).
* **Cursor:** Um objeto cursor é criado a partir da conexão (`cursor = conn.cursor()`) e é usado para executar comandos SQL.
* **Execução de SQL:**
    * `cursor.execute("SELECT * FROM tabela")` para consultas.
    * `cursor.execute("INSERT INTO tabela (col1, col2) VALUES (?, ?)", valor1, valor2)` para inserções parametrizadas (previne SQL injection).
    * Para DML (INSERT, UPDATE, DELETE), é necessário chamar `conn.commit()` para persistir as alterações. Em caso de erro, `conn.rollback()` pode ser usado.
* **Busca de Resultados:** `cursor.fetchone()`, `cursor.fetchall()`, ou iterando sobre o cursor.
* **Fechamento:** É importante fechar o cursor e a conexão (`cursor.close()`, `conn.close()`) após o uso, preferencialmente em blocos `try...finally`.

**Vantagens:**
* Abstração do SGBD (teoricamente, pode-se mudar o banco de dados com poucas alterações no código, se o SQL for padrão).
* Amplamente suportado e maduro.

**Desvantagens:**
* Requer instalação e configuração de drivers ODBC no sistema.
* Mais verboso para operações CRUD comparado a ORMs.
* O desenvolvedor ainda lida diretamente com SQL.

## ORM em Python com Django

ORM (Object-Relational Mapping) é uma técnica de desenvolvimento que faz a ponte entre o modelo de objetos de linguagens como Python e as tabelas de um banco de dados relacional. Em vez de escrever SQL diretamente, você manipula objetos Python — criando, lendo, atualizando ou removendo instâncias — e o ORM converte essas operações em comandos SQL equivalentes. Assim, o banco de dados é acessado de forma mais intuitiva, seguindo os mesmos princípios de orientação a objetos usados no restante da aplicação.

**Framework Utilizado: Django ORM**

O Django, um framework web de alto nível para Python, inclui um ORM poderoso e intuitivo. Com o Django ORM, você define seus modelos de dados como classes Python, e o ORM cuida da tradução dessas definições e operações para comandos SQL.

**Principais Conceitos e Funcionamento no Django ORM:**

1.  **Models (`models.py`):**
    * Cada modelo é uma classe Python que herda de `django.db.models.Model`.
    * Cada classe de modelo representa uma tabela no banco de dados.
    * Cada atributo da classe (campo do modelo, como `CharField`, `IntegerField`, `DateField`, `ForeignKey`, `ManyToManyField`) representa uma coluna na tabela.
    * Exemplo:
        ```python
        from django.db import models

        class Departamento(models.Model):
            nome = models.CharField(max_length=100)
            sigla = models.CharField(max_length=10, unique=True)

        class Funcionario(models.Model):
            nome = models.CharField(max_length=150)
            salario = models.DecimalField(max_digits=10, decimal_places=2) # Exemplo, Django usa DecimalField para dinheiro
            depto = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
        ```

2.  **Consultas (QuerySets):**
    * O Django fornece uma API de acesso ao banco de dados rica e abstrata através do "manager" de cada modelo (por padrão, `Model.objects`).
    * Você não escreve SQL diretamente (na maioria dos casos). Em vez disso, usa métodos Python:
        * `Departamento.objects.all()`: Retorna todos os departamentos.
        * `Departamento.objects.filter(sigla='DHC')`: Retorna departamentos com sigla 'DHC'.
        * `Departamento.objects.get(id=1)`: Retorna o departamento com id 1 (levanta exceção se não encontrar ou encontrar múltiplos).
        * `novo_depto = Departamento.objects.create(nome='Novo Depto', sigla='NDP')`: Cria um novo departamento.
        * `depto_para_atualizar.nome = 'Nome Atualizado'; depto_para_atualizar.save()`: Atualiza um departamento.
        * `depto_para_deletar.delete()`: Deleta um departamento.
    * As consultas retornam `QuerySet`s, que são coleções de objetos que podem ser iteradas, fatiadas, e encadeadas com mais filtros. São "lazy" (preguiçosas), ou seja, a consulta ao banco de dados só é realmente executada quando o QuerySet é avaliado.

3.  **Migrations:**
    * O Django possui um sistema de migrações robusto. Quando você altera seus modelos (adiciona um campo, remove um modelo, etc.), você executa:
        * `python manage.py makemigrations`: Cria os arquivos de migração que descrevem as alterações no esquema.
        * `python manage.py migrate`: Aplica essas migrações ao banco de dados.
    * Isso mantém o esquema do seu banco de dados sincronizado com seus modelos Python de forma controlada e versionada.

**Vantagens do Django ORM:**
* **Desenvolvimento Rápido:** Reduz significativamente a quantidade de código boilerplate para operações CRUD.
* **Abstração de SQL:** Escreve-se Python, não SQL, tornando o código mais legível para desenvolvedores Python.
* **Portabilidade:** Facilita a troca do SGBD de backend (ex: de SQLite para PostgreSQL) com poucas ou nenhuma alteração no código dos modelos/consultas.
* **Segurança:** Ajuda a prevenir ataques de injeção de SQL, pois as consultas são construídas de forma segura.
* **Integração:** Totalmente integrado ao restante do framework Django (admin, forms, etc.).

**Desvantagens:**
* **Curva de Aprendizado:** Entender todos os recursos e otimizações do ORM pode levar tempo.
* **Overhead:** Para consultas extremamente complexas ou que exigem otimizações de desempenho muito específicas, o SQL gerado pelo ORM pode não ser o mais eficiente. Nesses casos, o Django permite executar SQL bruto.
* **"Magia":** Às vezes, pode parecer que o ORM faz "mágica", e entender o que acontece por baixo dos panos é importante para depuração e otimização.