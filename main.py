import pymysql
from faker import Faker
import random

fake = Faker('pt_BR')

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="PMFS_AMAZONAS"
    )

def inserir_detentores(cursor, quantidade=50):
    for _ in range(quantidade):
        documento = fake.unique.cnpj()
        tipo_pessoa = random.choice(["Física", "Jurídica"])
        nome = fake.name() if tipo_pessoa == "Física" else fake.company()
        cursor.execute("""
            INSERT INTO DETENTOR (ID_DETENTOR, DOCUMENTO_DETENTOR, TIPO_PESSOA_DETENTOR, NOME_DETENTOR)
            VALUES (%s, %s, %s, %s)
        """, (_+1, documento, tipo_pessoa, nome))

def inserir_ambientes(cursor, quantidade=20):
    for _ in range(quantidade):
        bioma = f"{fake.word()}_{_}"  # Sempre único
        clima = random.choice(["Equatorial", "Tropical", "Subtropical"])
        solo = fake.text(max_nb_chars=50)
        fitofisionomia = fake.word()
        cursor.execute("""
            INSERT INTO AMBIENTE (BIOMA, CLIMA, SOLO, FITOFISIONOMIA)
            VALUES (%s, %s, %s, %s)
        """, (bioma, clima, solo, fitofisionomia))

def inserir_silvicultura(cursor, quantidade=20):
    for _ in range(quantidade):
        metodo = fake.word()
        sistema = fake.word()
        ciclo = round(random.uniform(1, 10), 2)
        area_total = round(random.uniform(1000, 5000), 2)
        area_manejo = round(random.uniform(500, area_total), 2)
        area_efetivo = round(random.uniform(100, area_manejo), 2)
        capacidade = round(random.uniform(50, 500), 2)
        estimativa = round(random.uniform(50, 500), 2)
        intensidade = round(random.uniform(0.5, 5), 2)
        tipo_volume = random.choice(["m³", "toneladas"])
        formula_volume = "Fórmula " + fake.word()
        cursor.execute("""
            INSERT INTO SILVICULTURA (METODO_EXTRACAO, SISTEMA_SILVICULTURAL, CICLO_CORTE, AREA_TOTAL_PROPRIEDADE,
                                      AREA_MANEJO_FLORESTAL, AREA_EFETIVO_MANEJO, CAPACIDADE_PRODUTIVA,
                                      ESTIMATIVA_PRODUTIVA_ANUAL, INTENSIDADE_CORTE, TIPO_VOLUME, FORMULA_VOLUME)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (metodo, sistema, ciclo, area_total, area_manejo, area_efetivo, capacidade, estimativa, intensidade, tipo_volume, formula_volume))

def inserir_empresamento_tipo(cursor, quantidade=20):
    for i in range(quantidade):
        tipo = f"Empreendimento {i+1}"  # Sempre único
        natureza = random.choice(["Privada", "Pública", "Mista"])
        competencia = fake.word()
        orgao = fake.company()
        cursor.execute("""
            INSERT INTO EMPREENDIMENTO_TIPO (TIPO_DE_EMPREENDIMENTO, NATUREZA_JURIDICA, COMPETENCIA_DA_AVALIACAO, ORGAO_AMBIENTAL_RESP_ANALISE)
            VALUES (%s,%s,%s,%s)
        """, (tipo, natureza, competencia, orgao))

def inserir_estado(cursor):
    estados = [("AM", "Amazonas"), ("SP", "São Paulo"), ("RJ", "Rio de Janeiro")]
    for i, (uf, nome) in enumerate(estados, start=1):
        cursor.execute("""
            INSERT INTO ESTADO (ID_ESTADO, UF, NOME_ESTADO_REGISTRO)
            VALUES (%s,%s,%s)
        """, (i, uf, nome))

def inserir_cnaes(cursor, quantidade=20):
    for _ in range(quantidade):
        codigo = str(1000 + _)
        descricao = "Atividade " + fake.word()
        cursor.execute("""
            INSERT INTO CNAES (CODIGO_CNAE_FISCAL, DESCRICAO_CNAE_FISCAL)
            VALUES (%s,%s)
        """, (codigo, descricao))

def inserir_responsavel_tecnico(cursor, quantidade=20):
    for _ in range(quantidade):
        nro_art = str(1000 + _)
        nome = fake.name()
        atividade = fake.word()
        cursor.execute("""
            INSERT INTO RESPONSAVEL_TECNICO (NRO_ART, NOME_DO_RT, ATIVIDADE_RT)
            VALUES (%s,%s,%s)
        """, (nro_art, nome, atividade))

def inserir_pmfs_modalidade(cursor, quantidade=10):
    for _ in range(quantidade):
        modalidade = "Modalidade " + fake.word()
        cursor.execute("""
            INSERT INTO PMFS_MODALIDADE (MODALIDADE_PMFS)
            VALUES (%s)
        """, (modalidade,))

def inserir_municipios(cursor, quantidade=10):
    estados = [("AM", "Amazonas"), ("SP", "São Paulo"), ("RJ", "Rio de Janeiro")]
    for _ in range(quantidade):
        nome = fake.city()
        uf = random.choice(estados)[0]
        cursor.execute("""
            INSERT INTO MUNICIPIO (NOME_MUNICIPIO, UF)
            VALUES (%s, %s)
        """, (nome, uf))

def inserir_imoveis(cursor, quantidade=10):
    cursor.execute("SELECT ID_MUNICIPIO FROM MUNICIPIO")
    municipios = [row[0] for row in cursor.fetchall()]
    for _ in range(quantidade):
        nro_car = "CAR" + str(1000 + _)
        vinculado = fake.company()
        nome_emp = fake.company()
        latitude = round(random.uniform(-5, -1), 6)
        id_municipio = random.choice(municipios)
        cursor.execute("""
            INSERT INTO IMOVEL (NRO_CAR_IMOVEL_RURAL, IMOVEL_RURAL_VINCULADO, NOME_EMPREENDIMENTO_VINC, LATITUDE_EMPREENDIMENTO, ID_MUNICIPIO)
            VALUES (%s, %s, %s, %s, %s)
        """, (nro_car, vinculado, nome_emp, latitude, id_municipio))

def inserir_projetos(cursor, quantidade=500):
    cursor.execute("SELECT ID_DETENTOR FROM DETENTOR")
    detentores = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_EMPREENDIMENTO_TIPO FROM EMPREENDIMENTO_TIPO")
    empreendimentos = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_AMBIENTE FROM AMBIENTE")
    ambientes = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_SILVICULTURA FROM SILVICULTURA")
    silviculturas = [row[0] for row in cursor.fetchall()]
    for _ in range(quantidade):
        nro_registro = 10000 + _
        data_emissao = fake.date_between('-2y', 'today')
        nro_autorizacao = random.randint(100000, 999999)
        ano_autorizacao = random.randint(2020, 2025)
        descricao = fake.text(50)
        data_validade = fake.date_between('today', '+2y')
        id_detentor = random.choice(detentores)
        id_empreendimento = random.choice(empreendimentos)
        id_ambiente = random.choice(ambientes)
        id_silvicultura = random.choice(silviculturas)
        situacao = random.choice(["Ativo", "Inativo", "Suspenso"])
        data_situacao = fake.date_between('-1y', 'today')
        tramite = fake.word()
        data_tramite = fake.date_between('-1y', 'today')
        ultima_atualizacao = fake.date_between('-1y', 'today')
        cursor.execute("""
            INSERT INTO PROJETO (NRO_REGISTRO, DATA_DE_EMISSAO, NRO_AUTORIZACAO, ANO_AUTORIZACAO, DESCRICAO_AUTORIZACAO,
                                 DATA_DE_VALIDADE, ID_DETENTOR, ID_EMPREENDIMENTO, ID_AMBIENTE, ID_SILVICULTURA,
                                 SITUACAO, DATA_SITUACAO, ULTIMO_TRAMITE, DATA_DO_TRAMITE, ULTIMA_ATUALIZACAO_RELATORIO)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nro_registro, data_emissao, nro_autorizacao, ano_autorizacao, descricao, data_validade, id_detentor, id_empreendimento, id_ambiente, id_silvicultura, situacao, data_situacao, tramite, data_tramite, ultima_atualizacao))

def inserir_projeto_pmfs_modalidade(cursor, quantidade=10):
    cursor.execute("SELECT NRO_REGISTRO FROM PROJETO")
    projetos = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_PMFS_MODALIDADE FROM PMFS_MODALIDADE")
    modalidades = [row[0] for row in cursor.fetchall()]
    for _ in range(quantidade):
        nro_registro = random.choice(projetos)
        id_modalidade = random.choice(modalidades)
        cursor.execute("""
            INSERT INTO PROJETO_PMFS_MODALIDADE (NRO_REGISTRO, ID_PMFS_MODALIDADE)
            VALUES (%s, %s)
        """, (nro_registro, id_modalidade))

def inserir_projeto_imovel(cursor, quantidade=10):
    cursor.execute("SELECT NRO_REGISTRO FROM PROJETO")
    projetos = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_IMOVEL FROM IMOVEL")
    imoveis = [row[0] for row in cursor.fetchall()]
    for _ in range(quantidade):
        nro_registro = random.choice(projetos)
        id_imovel = random.choice(imoveis)
        cursor.execute("""
            INSERT INTO PROJETO_IMOVEL (NRO_REGISTRO, ID_IMOVEL)
            VALUES (%s, %s)
        """, (nro_registro, id_imovel))

def inserir_projeto_responsavel_tecnico(cursor, quantidade=10):
    cursor.execute("SELECT NRO_REGISTRO FROM PROJETO")
    projetos = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT ID_RESPONSAVEL_TECNICO FROM RESPONSAVEL_TECNICO")
    tecnicos = [row[0] for row in cursor.fetchall()]
    for _ in range(quantidade):
        nro_registro = random.choice(projetos)
        id_tecnico = random.choice(tecnicos)
        cursor.execute("""
            INSERT INTO PROJETO_RESPONSAVEL_TECNICO (ID_PROJETO_RT, NRO_REGISTRO, ID_RESPONSAVEL_TECNICO)
            VALUES (%s, %s, %s)
        """, (_+1, nro_registro, id_tecnico))

def inserir_empresas(cursor, quantidade=10):
    cursor.execute("SELECT DOCUMENTO_DETENTOR FROM DETENTOR WHERE TIPO_PESSOA_DETENTOR='Jurídica'")
    cnpjs = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT CODIGO_CNAE_FISCAL FROM CNAES")
    cnaes = [row[0] for row in cursor.fetchall()]
    for _ in range(min(quantidade, len(cnpjs))):
        cnpj = cnpjs[_]
        nome_fantasia = fake.company()
        razao = fake.company_suffix()
        situacao = random.choice(["Ativa", "Inativa"])
        data_inicio = fake.date_between('-10y', 'today')
        codigo_cnae = random.choice(cnaes)
        cursor.execute("""
            INSERT INTO EMPRESA (CNPJ, NOME_FANTASIA, RAZAO, SITUACAO_CADASTRAL, DATA_INICIO_ATIVIDADE, CODIGO_CNAE_FISCAL)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (cnpj, nome_fantasia, razao, situacao, data_inicio, codigo_cnae))

def limpar_tabelas(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    tabelas = [
        "EMPRESA",
        "PROJETO_RESPONSAVEL_TECNICO",
        "PROJETO_IMOVEL",
        "PROJETO_PMFS_MODALIDADE",
        "PROJETO",
        "IMOVEL",
        "MUNICIPIO",
        "ESTADO",
        "PMFS_MODALIDADE",
        "RESPONSAVEL_TECNICO",
        "CNAES",
        "EMPREENDIMENTO_TIPO",
        "SILVICULTURA",
        "AMBIENTE",
        "DETENTOR"
    ]
    for tabela in tabelas:
        cursor.execute(f"TRUNCATE TABLE {tabela};")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

if __name__ == "__main__":
    conn = connect_db()
    cursor = conn.cursor()

    limpar_tabelas(cursor)  # Limpa todas as tabelas

    inserir_detentores(cursor)
    inserir_ambientes(cursor)
    inserir_silvicultura(cursor)
    inserir_empresamento_tipo(cursor)
    inserir_estado(cursor)
    inserir_cnaes(cursor)
    inserir_responsavel_tecnico(cursor)
    inserir_pmfs_modalidade(cursor)
    inserir_municipios(cursor)
    inserir_imoveis(cursor)
    inserir_projetos(cursor)
    inserir_projeto_pmfs_modalidade(cursor)
    inserir_projeto_imovel(cursor)
    inserir_projeto_responsavel_tecnico(cursor)
    inserir_empresas(cursor)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Todas as 15 tabelas foram limpas e populadas com sucesso!")