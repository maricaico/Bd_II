import pyodbc
import sys
import os 
from dotenv import load_dotenv 

load_dotenv()

db_driver = os.getenv("DB_DRIVER")
db_server = os.getenv("DB_SERVER")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

if not all([db_driver, db_server, db_port, db_database, db_username, db_password]):
    print("ERRO: Uma ou mais variáveis de ambiente do banco de dados não estão definidas.")
    print("Verifique seu arquivo .env ou as variáveis de ambiente do sistema.")
    sys.exit(1)

conn_str = (
    f"DRIVER={db_driver};"
    f"SERVER={db_server};"
    f"PORT={db_port};"
    f"DATABASE={db_database};"
    f"UID={db_username};"
    f"PWD={db_password};"
)

conn = None
try:
    print(f"Conectando ao banco de dados '{db_database}' no servidor '{db_server}'...")
    conn = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida!")

    cursor = conn.cursor()

    print("\nListando departamentos (exemplo):")
    cursor.execute("SELECT codigo, nome, sigla FROM departamento ORDER BY nome;")

    if cursor.rowcount == 0:
        print("Nenhum departamento encontrado.")
    else:
        for row in cursor.fetchall():
            print(f" - Código: {row.codigo}, Nome: {row.nome}, Sigla: {row.sigla}")

    print("\n--- 1. Inserindo nova atividade ---")
    try:
        nova_descricao_atividade = "Reunião de Definição de Escopo Adicional"
        projeto_id_para_nova_atividade = 1 
        data_inicio_nova_atividade = "2025-07-01"
        data_fim_nova_atividade = "2025-07-05"

        sql_insert_atividade = """
            INSERT INTO atividade (descricao, projeto, data_inicio, data_fim)
            VALUES (?, ?, ?, ?);
        """
        cursor.execute(sql_insert_atividade,
                       nova_descricao_atividade,
                       projeto_id_para_nova_atividade,
                       data_inicio_nova_atividade,
                       data_fim_nova_atividade)
        conn.commit() 
        print(f"Nova atividade '{nova_descricao_atividade}' inserida com sucesso no projeto ID {projeto_id_para_nova_atividade}.")

    except pyodbc.Error as ex_insert:
        sqlstate = ex_insert.args[0]
        print(f"ERRO ao inserir atividade: {sqlstate} - {ex_insert}")
        if conn:
            conn.rollback() 

    print("\n--- 2. Atualizando líder de projeto ---")
    try:
        projeto_id_para_atualizar_lider = 2 
        novo_lider_id = 3                   

        cursor.execute("SELECT responsavel FROM projeto WHERE codigo = ?", projeto_id_para_atualizar_lider)
        lider_antigo_row = cursor.fetchone()
        if lider_antigo_row:
            print(f"Líder antigo do projeto ID {projeto_id_para_atualizar_lider}: {lider_antigo_row[0]}")
        else:
            print(f"Projeto ID {projeto_id_para_atualizar_lider} não encontrado para verificar líder antigo.")

        sql_update_lider = """
            UPDATE projeto SET responsavel = ? WHERE codigo = ?;
        """
        cursor.execute(sql_update_lider, novo_lider_id, projeto_id_para_atualizar_lider)
        
        if cursor.rowcount > 0:
            conn.commit() 
            print(f"Líder do projeto ID {projeto_id_para_atualizar_lider} atualizado para funcionário ID {novo_lider_id} com sucesso.")
            cursor.execute("SELECT responsavel FROM projeto WHERE codigo = ?", projeto_id_para_atualizar_lider)
            lider_novo_row = cursor.fetchone()
            if lider_novo_row:
                 print(f"Novo líder do projeto ID {projeto_id_para_atualizar_lider}: {lider_novo_row[0]}")
        else:
            print(f"Nenhum projeto encontrado com ID {projeto_id_para_atualizar_lider} para atualizar o líder, ou o líder já era o ID {novo_lider_id}.")

    except pyodbc.Error as ex_update:
        sqlstate = ex_update.args[0]
        print(f"ERRO ao atualizar líder do projeto: {sqlstate} - {ex_update}")
        if conn:
            conn.rollback()

    print("\n--- 3. Listando todos os projetos e suas atividades ---")
    try:
        sql_listar_projetos_atividades = """
            SELECT
                p.codigo AS projeto_codigo,
                p.nome AS projeto_nome,
                a.codigo AS atividade_codigo,
                a.descricao AS atividade_descricao,
                a.data_inicio AS atividade_data_inicio,
                a.data_fim AS atividade_data_fim
            FROM
                projeto p
            LEFT JOIN -- Usamos LEFT JOIN para listar projetos mesmo que não tenham atividades
                atividade a ON p.codigo = a.projeto
            ORDER BY
                p.nome, a.data_inicio;
        """
        cursor.execute(sql_listar_projetos_atividades)

        projetos_listados = {}
        for row in cursor.fetchall():
            if row.projeto_codigo not in projetos_listados:
                projetos_listados[row.projeto_codigo] = {
                    'nome': row.projeto_nome,
                    'atividades': []
                }
            if row.atividade_codigo: 
                projetos_listados[row.projeto_codigo]['atividades'].append(
                    f"  - AtivID {row.atividade_codigo}: {row.atividade_descricao} (Início: {row.atividade_data_inicio}, Fim: {row.atividade_data_fim})"
                )
        
        if not projetos_listados:
            print("Nenhum projeto encontrado.")
        else:
            for proj_id, proj_data in projetos_listados.items():
                print(f"\nProjeto: {proj_data['nome']} (ID: {proj_id})")
                if proj_data['atividades']:
                    for atividade_info in proj_data['atividades']:
                        print(atividade_info)
                else:
                    print("  - (Nenhuma atividade cadastrada para este projeto)")

    except pyodbc.Error as ex_select:
        sqlstate = ex_select.args[0]
        print(f"ERRO ao listar projetos e atividades: {sqlstate} - {ex_select}")
    cursor.close()

except pyodbc.Error as ex_insert:
        sqlstate = ex_insert.args[0]
        print(f"ERRO ao inserir atividade: {sqlstate} - {ex_insert}")
        if conn:
            conn.rollback() 

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"\nERRO ao conectar ou executar SQL: {sqlstate}")
    print(ex)
    if conn:
        conn.close()
    sys.exit(1)

finally:
    if conn:
        print("\nFechando conexão com o banco de dados.")
        conn.close()