# Bd_II

## Repositório destinado a disciplina de Projeto e Administração de Banco de Dados

### Aluna: Mariana dos Santos Batista Medeiros

### Matrícula: 20230083988

### Email: mari_caico@yahoo.com.br


### * [Tarefa 01](./tarefas/t01/tarefa01.md)

### * [Tarefa ‑ ODBC e ORM](./tarefas/orm/tarefa-orm.md)


## Executando os Scripts de Demonstração (ODBC e ORM)

Esta seção descreve como configurar o ambiente e executar os scripts Python de exemplo (`programa_odbc.py` e `programa_orm_django.py`) que interagem com o banco de dados `atividadesbd`.

### Pré-requisitos

1.  **Python 3.x instalado.**
2.  **PostgreSQL instalado e em execução.**
3.  **Banco de Dados Configurado:**
    * O banco de dados (`atividadesbd`) deve estar criado no PostgreSQL.
    * Um usuário com permissão para acessar este banco deve existir.
    * As tabelas e os dados iniciais devem ser criados/populados executando o script SQL:
        `tarefas/orm/scripts_db/schema_e_dados_atividadesbd.sql`
        (Você pode executar este script usando uma ferramenta como DBeaver ou via `psql` no terminal).
4.  **Para `programa_odbc.py` (Linux/Ubuntu):**
    * Driver ODBC do PostgreSQL: `sudo apt install odbc-postgresql`
    * Gerenciador unixODBC: `sudo apt install unixodbc unixodbc-dev`
    * Após a instalação, rode: `sudo ldconfig`

### Configuração do Ambiente do Projeto

1.  **Clone o repositório (se ainda não o fez):**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_Bd_II]
    cd Bd_II
    ```

2.  **Crie e ative um ambiente virtual Python:**
    (Recomendamos o nome `venv_db` como usado nos exemplos, mas pode ser qualquer nome)
    ```bash
    python3 -m venv venv_db
    source venv_db/bin/activate  # Para Linux/macOS
    # No Windows, seria: .\venv_db\Scripts\activate
    ```

3.  **Instale as dependências Python:**
    As dependências necessárias são `pyodbc`, `django`, `psycopg2-binary` e `python-dotenv`. Você pode instalá-las individualmente ou, idealmente, a partir de um arquivo `requirements.txt`.

    * **Opção A (Recomendado - com `requirements.txt`):**
        Crie um arquivo chamado `requirements.txt` na raiz do projeto `Bd_II` com o seguinte conteúdo:
        ```
        pyodbc
        django
        psycopg2-binary
        python-dotenv
        ```
        Depois, instale as dependências com:
        ```bash
        pip install -r requirements.txt
        ```

    * **Opção B (Instalação individual):**
        ```bash
        pip install pyodbc django psycopg2-binary python-dotenv
        ```

4.  **Configure as Variáveis de Ambiente para o Banco de Dados:**
    * Navegue até a pasta dos scripts: `cd tarefas/orm/`
    * Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
        ```bash
        cp .env.example .env
        ```
    * Abra o arquivo `.env` recém-criado em um editor de texto.
    * Substitua os valores placeholder pelas suas credenciais reais do banco de dados PostgreSQL:
        ```ini
        DB_DRIVER="{PostgreSQL Unicode}" # Ou o driver ODBC correto para seu sistema
        DB_SERVER="localhost"
        DB_PORT="5432" # Ou a porta que seu PostgreSQL está usando
        DB_DATABASE="atividadesbd" # Ou o nome exato do seu banco
        DB_USERNAME="seu_usuario_pg"
        DB_PASSWORD="sua_senha_pg"
        ```
    * Salve o arquivo `.env`. **Este arquivo não deve ser commitado no Git** (garanta que `.env` e `*.env` estejam no seu `.gitignore`).

### Executando os Scripts

Após a configuração acima e com o ambiente virtual ativado:

1.  **Navegue até a pasta dos scripts (se não estiver lá):**
    (A partir da raiz `Bd_II/`)
    ```bash
    cd tarefas/orm/
    ```

2.  **Para executar o script ODBC:**
    ```bash
    python programa_odbc.py
    ```

3.  **Para executar o script ORM Django:**
    ```bash
    python programa_orm_django.py
    ```




