import os
import django
from django.conf import settings
from django.db import models
from dotenv import load_dotenv
import datetime


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    project_root_env_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(project_root_env_path):
        load_dotenv(project_root_env_path)
    else:
        print("Aviso: arquivo .env não encontrado nos caminhos esperados.")

if not settings.configured:
    DB_ENGINE = 'django.db.backends.postgresql'
    DB_NAME = os.getenv("DB_DATABASE")
    DB_USER = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_SERVER")
    DB_PORT = os.getenv("DB_PORT")

    if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
        print("ERRO: Variáveis de ambiente do banco de dados não estão completamente definidas.")
        print("Verifique: DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT")
        exit()

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': DB_ENGINE,
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': DB_HOST,
                'PORT': DB_PORT,
            }
        },
        INSTALLED_APPS=[
            '__main__',
        ],
        USE_TZ=False,
    )
    django.setup()

class Departamento(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    sigla = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.sigla} - {self.nome if self.nome else 'Sem Nome'}"

    class Meta:
        db_table = 'departamento'
        managed = False

class Funcionario(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    dt_nasc = models.DateField(null=True, blank=True)
    salario = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados', db_column='supervisor') # CORREÇÃO
    depto = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionarios_do_depto', db_column='depto') # CORREÇÃO

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'funcionario'
        managed = False

Departamento.add_to_class('gerente', models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='departamento_gerenciado_por_mim', db_column='gerente')) # CORREÇÃO

class Projeto(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=250, null=True, blank=True)
    responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos_liderados', db_column='responsavel') # CORREÇÃO
    depto = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos_do_depto', db_column='depto') # CORREÇÃO
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'projeto'
        managed = False

class Atividade(models.Model):
    codigo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=250)
    projeto = models.ForeignKey(Projeto, on_delete=models.SET_NULL, null=True, blank=True, related_name='atividades_do_projeto', db_column='projeto') # CORREÇÃO
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'atividade'
        managed = False

def inserir_atividade_orm():
    print("\n--- 1. Inserindo nova atividade via ORM ---")
    try:
        projeto_es = Projeto.objects.get(codigo=4) 

        nova_atividade = Atividade.objects.create(
            descricao="Elaboração Diagrama de Classes - ORM",
            projeto=projeto_es,
            data_inicio=datetime.date(2025, 11, 1),
            data_fim=datetime.date(2025, 11, 15)
        )
        print(f"Nova atividade '{nova_atividade.descricao}' (ID: {nova_atividade.codigo}) inserida com sucesso no projeto '{projeto_es.nome}'.")
    except Projeto.DoesNotExist:
        print(f"ERRO: Projeto com código 4 (ES) não encontrado para inserir atividade.")
    except Exception as e:
        print(f"ERRO ao inserir atividade via ORM: {e}")

def atualizar_lider_projeto_orm():
    print("\n--- 2. Atualizando líder de projeto via ORM ---")
    try:
        projeto_apf = Projeto.objects.get(codigo=1) 
        novo_lider_carlos = Funcionario.objects.get(codigo=5) 

        responsavel_antigo_nome = projeto_apf.responsavel.nome if projeto_apf.responsavel else "Nenhum"
        print(f"Líder antigo do projeto '{projeto_apf.nome}': {responsavel_antigo_nome}")

        projeto_apf.responsavel = novo_lider_carlos
        projeto_apf.save()

        print(f"Líder do projeto '{projeto_apf.nome}' atualizado para '{novo_lider_carlos.nome}' com sucesso.")
    except Projeto.DoesNotExist:
        print(f"ERRO: Projeto com código 1 (APF) não encontrado.")
    except Funcionario.DoesNotExist:
        print(f"ERRO: Funcionário com código 5 (Carlos) não encontrado.")
    except Exception as e:
        print(f"ERRO ao atualizar líder do projeto via ORM: {e}")

def listar_projetos_atividades_orm():
    print("\n--- 3. Listando todos os projetos e suas atividades via ORM ---")
    try:
        todos_projetos = Projeto.objects.prefetch_related('atividades_do_projeto', 'responsavel', 'depto__gerente').all().order_by('nome')

        if not todos_projetos:
            print("Nenhum projeto encontrado.")
        else:
            for p in todos_projetos:
                lider_nome = p.responsavel.nome if p.responsavel else "N/A"
                depto_sigla = p.depto.sigla if p.depto else "N/A"
                gerente_depto_nome = "N/A"
                if p.depto and p.depto.gerente:
                    gerente_depto_nome = p.depto.gerente.nome

                print(f"\nProjeto: {p.nome} (ID: {p.codigo}) - Depto: {depto_sigla} (Gerente: {gerente_depto_nome}) - Líder Proj: {lider_nome}")

                atividades = p.atividades_do_projeto.all().order_by('data_inicio', 'codigo')
                if atividades:
                    for a in atividades:
                        print(f"  - AtivID {a.codigo}: {a.descricao} (Início: {a.data_inicio}, Fim: {a.data_fim})")
                else:
                    print("  - (Nenhuma atividade cadastrada para este projeto)")
    except Exception as e:
        print(f"ERRO ao listar projetos e atividades via ORM: {e}")

if __name__ == '__main__':
    print("Executando script com Django ORM...")
    if settings.configured:
        print(f"Usando banco de dados: {settings.DATABASES['default']['NAME']} no host {settings.DATABASES['default']['HOST']}")
    else:
        print("ERRO FATAL: As configurações do Django não foram carregadas.")
        exit()
    
    inserir_atividade_orm()
    atualizar_lider_projeto_orm()

    print("\n--- Estado APÓS as operações de INSERT e UPDATE ---")
    listar_projetos_atividades_orm()

    print("\n--- Operações ORM concluídas ---")