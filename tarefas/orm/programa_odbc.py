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
    cursor.close()

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