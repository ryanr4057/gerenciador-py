import sqlite3
from datetime import datetime

conn = sqlite3.connect(f'banco_de_dados.sqlite3')

conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

def cria_tabela_membro():
    c.execute('''CREATE TABLE membro (
                    id_membro INTEGER PRIMARY KEY,
                    nome TEXT UNIQUE,
                    funcao TEXT
                 )''')
    conn.commit()

def cria_tabela_habilidade():
    c.execute('''CREATE TABLE habilidade (
                    id_habilid INTEGER PRIMARY KEY,
                    nome TEXT UNIQUE
                 )''')
    conn.commit()

def cria_tabela_hab_memb():
    c.execute('''CREATE TABLE membro_habilidade (
                    id_habilid INTEGER NOT NULL,
                    id_membro INTEGER NOT NULL,
                    FOREIGN KEY (id_habilid) REFERENCES habilidade(id_habilid),
                    FOREIGN KEY (id_membro) REFERENCES membro(id_membro),
                    PRIMARY KEY (id_habilid, id_membro)
                 )''')
    conn.commit()

def cria_tabela_projeto():
    c.execute('''CREATE TABLE projeto (
                    id_proj INTEGER PRIMARY KEY,
                    nome TEXT,
                    descric TEXT,
                    data_ini DATE,
                    data_term DATE,
                    status TEXT CHECK (status IN ('em andamento', 'concluido', 'cancelado')),
                    respons INTEGER NOT NULL,
                    FOREIGN KEY (respons) REFERENCES membro(id_membro)
                 )''')
    conn.commit()

def cria_tabela_tarefa():
    c.execute('''CREATE TABLE tarefa (
                    id_taref INTEGER PRIMARY KEY,
                    descric TEXT,
                    data_ini DATE,
                    data_term DATE,
                    status TEXT CHECK (status IN ('em andamento', 'concluida', 'pendente')),
                    respons INTEGER NOT NULL,
                    proj_assoc INTEGER NOT NULL,
                    FOREIGN KEY (proj_assoc) REFERENCES projeto(id_proj),
                    FOREIGN KEY (respons) REFERENCES membro(id_membro)
                 )''')
    conn.commit()

def cria_tabela_proj_memb():
    c.execute('''CREATE TABLE membros_projeto (
                    id_proj INTEGER NOT NULL,
                    id_membro INTEGER NOT NULL,
                    FOREIGN KEY (id_proj) REFERENCES projeto(id_proj),
                    FOREIGN KEY (id_membro) REFERENCES membro(id_membro),
                    PRIMARY KEY (id_proj, id_membro)
                 )''')
    conn.commit()

def cria_tabela_documentos():
    c.execute('''CREATE TABLE documento (
                    id_doc INTEGER PRIMARY KEY,
                    nome TEXT,
                    descric TEXT,
                    data_cri DATE,
                    versao TEXT,
                    id_proj INTEGER NOT NULL,
                    FOREIGN KEY (id_proj) REFERENCES projeto(id_proj)
                 )''')
    conn.commit()

def cria_tabela_relatorios():
    c.execute('''CREATE TABLE relatorio (
                    id_relat INTEGER PRIMARY KEY,
                    data_ger DATE,
                    tipo TEXT,
                    id_proj INTEGER NOT NULL,
                    FOREIGN KEY (id_proj) REFERENCES projeto(id_proj)
                 )''')
    conn.commit()

def inserir_membro(nome, funcao):
    c.execute("INSERT INTO membro (nome, funcao) VALUES (?, ?)", (nome, funcao))
    conn.commit()

def inserir_habilidade(nome):
    c.execute("INSERT INTO habilidade (nome) VALUES (?)", (nome,))
    conn.commit()

def inserir_habilidade_membro(nome_membro, nome_habilidade):
    id_membro = buscar_membro_id(nome_membro)
    id_habilidade = buscar_habilidade_id(nome_habilidade)
    c.execute("INSERT INTO membro_habilidade (id_habilid, id_membro) VALUES (?, ?)", (id_habilidade[0], id_membro[0]))
    conn.commit()

def inserir_projeto(nome, descric, data_ini, data_term, status, nome_respons):
    id_respons = buscar_membro_id(nome_respons)
    c.execute("INSERT INTO projeto (nome, descric, data_ini, data_term, status, respons) VALUES (?, ?,?, ?, ?, ?)", (nome, descric, data_ini, data_term, status, id_respons[0]))
    conn.commit()
    inserir_membro_projeto(nome,nome_respons)

def inserir_tarefa(descric, data_ini, data_term, status, nome_respons, proj_assoc):
    id_respons = buscar_membro_id(nome_respons)
    id_proj = buscar_projeto_id(proj_assoc)
    c.execute("INSERT INTO tarefa (descric, data_ini, data_term, status, respons, proj_assoc) VALUES (?, ?, ?, ?, ?, ?)", (descric, data_ini, data_term, status, id_respons[0], id_proj[0]))
    conn.commit()

def inserir_membro_projeto(nome_proj, nome_membro):
    id_memb = buscar_membro_id(nome_membro)
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("INSERT INTO membros_projeto (id_proj, id_membro) VALUES (?, ?)", (id_proj[0], id_memb[0]))
    conn.commit()

def inserir_documento(nome, descric, data_cri, versao, nome_proj):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("INSERT INTO documento (nome, descric, data_cri, versao, id_proj) VALUES (?, ?, ?, ?, ?)", (nome, descric, data_cri, versao, id_proj[0]))
    conn.commit()

def inserir_relatorio(data_ger, tipo, nome_proj):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("INSERT INTO relatorio (data_ger, tipo, id_proj) VALUES (?, ?, ?)", (data_ger, tipo, id_proj[0]))
    conn.commit()

def editar_projeto_status(nome_proj, status):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("UPDATE projeto SET status = ? WHERE id_proj = ?", (status, id_proj[0]))
    conn.commit()

def editar_projeto_prazo(nome_proj, data):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("UPDATE projeto SET data_term = ? WHERE id_proj = ?", (data, id_proj[0]))
    conn.commit()

def editar_tarefa_prazo(id_tar, data):
    c.execute("UPDATE tarefa SET data_term = ? WHERE id_taref = ?", (data, id_tar))
    conn.commit()

def editar_projeto_respons(nome_proj, nome_membro):
    id_proj = buscar_projeto_id(nome_proj)
    id_memb = buscar_membro_id(nome_membro)
    c.execute("UPDATE projeto SET respons = ? WHERE id_proj = ?", (id_memb[0], id_proj[0]))
    conn.commit()

def editar_tarefa_status(id_tarefa, status):
    c.execute("UPDATE tarefa SET status = ? WHERE id_taref = ?", (status, id_tarefa))
    conn.commit()

def editar_tarefa_respons(id_tarefa, nome_membro):
    id_memb = buscar_membro_id(nome_membro)
    c.execute("UPDATE tarefa SET respons = ? WHERE id_taref = ?", (id_memb, id_tarefa))
    conn.commit()

def buscar_habilidade_id(nome_habilidade):
    c.execute("SELECT id_habilid FROM habilidade WHERE nome = (?)", (nome_habilidade,))
    return c.fetchone()

def buscar_membro_id(nome_membro):
    c.execute("SELECT id_membro FROM membro WHERE nome = (?)", (nome_membro,))
    return c.fetchone()

def buscar_projeto_id(nome_projeto):
    c.execute("SELECT id_proj FROM projeto WHERE nome = (?)", (nome_projeto,))
    return c.fetchone()

def buscar_all_projeto():
    c.execute("SELECT projeto.nome, membro.nome FROM projeto join membro on projeto.respons = membro.id_membro")
    return c.fetchall()

def buscar_all_projeto_n():
    c.execute("SELECT nome FROM projeto")
    return c.fetchall()

def buscar_all_tarefa_n():
    c.execute("SELECT id_taref FROM tarefa")
    return c.fetchall()

def buscar_all_tarefa():
    c.execute("SELECT tarefa.descric, membro.nome, projeto.nome FROM tarefa join membro on tarefa.respons = membro.id_membro join projeto on tarefa.proj_assoc = projeto.id_proj")
    return c.fetchall()

def buscar_all_membro():
    c.execute("SELECT nome FROM membro")
    return c.fetchall()

def buscar_all_membro_f():
    c.execute("SELECT * FROM membro")
    return c.fetchall()

def buscar_all_habilidade():
    c.execute("SELECT nome FROM habilidade")
    return c.fetchall()

def buscar_proj_status(status):
    c.execute("SELECT nome FROM projeto WHERE status = (?)", (status,))
    return c.fetchall()

def buscar_tarefas_concluidas(nome_proj):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("SELECT descric FROM tarefa WHERE proj_assoc = (?) AND status = 'concluida'", (id_proj[0],))
    return c.fetchall()

def buscar_tarefas_proj(nome_proj):
    id_proj = buscar_projeto_id(nome_proj)
    c.execute("SELECT descric FROM tarefa WHERE proj_assoc = (?)", (id_proj[0],))
    return c.fetchall()

def buscar_membros_habil(habilidade):
    c.execute("SELECT membro.nome FROM membro join membro_habilidade on membro.id_membro = membro_habilidade.id_membro join habilidade on habilidade.id_habilid = membro_habilidade.id_habilid  WHERE habilidade.nome = (?)", (habilidade,))
    return c.fetchall()

def buscar_hab_memb_all():
    c.execute("SELECT id_habilid, id_membro FROM membro_habilidade")
    return c.fetchall()

def buscar_proj_memb_all():
    c.execute("SELECT id_proj, id_membro FROM membros_projeto")
    return c.fetchall()

def buscar_proj_documentos(nome_proj):
    c.execute("SELECT documento.nome FROM documento join projeto on documento.id_proj = projeto.id_proj WHERE projeto.nome = (?)", (nome_proj,))
    return c.fetchall()

def buscar_proj_relatorios(nome_proj):
    c.execute("SELECT documento.nome FROM documento join projeto on documento.id_proj = projeto.id_proj WHERE projeto.nome = (?)", (nome_proj,))
    return c.fetchall()

def buscar_proj_atras():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT nome FROM projeto WHERE data_term > date(?) AND status = 'em andamento' ", (data_atual,))
    return c.fetchall()

def buscar_projetos_membro(nome_membro):
    c.execute("SELECT projeto.nome FROM projeto join membros_projeto on projeto.id_proj = membros_projeto.id_proj join membro on membros_projeto.id_membro = membro.id_membro WHERE membro.nome = (?)", (nome_membro,))
    return c.fetchall()

def buscar_membros_projeto(nome_projeto):
    c.execute("SELECT membro.nome, membro.funcao FROM membro join projeto on projeto.id_proj = membros_projeto.id_proj join membros_projeto on membro.id_membro = membros_projeto.id_membro WHERE projeto.nome = (?)", (nome_projeto,))
    return c.fetchall()

def cria_banco():
    cria_tabela_membro(),
    cria_tabela_habilidade(),
    cria_tabela_hab_memb(),
    cria_tabela_projeto(),
    cria_tabela_tarefa(),
    cria_tabela_proj_memb(),
    cria_tabela_documentos(),
    cria_tabela_relatorios(),

def valida_membro(nome):
    membros = buscar_all_membro()
    membros = retira_tup(membros)

    if (nome in membros) is False:
        nome = input("Membro invalido. Tente novamente: ").lower()
        nome = valida_membro(nome)

    return nome

def valida_habilidade(nome):
    habilidades = buscar_all_habilidade()
    habilidades = retira_tup(habilidades)

    if (nome in habilidades) is False:
        nome = input("Habilidade invalida. Tente novamente: ").lower()
        nome = valida_habilidade(nome)

    return nome

def valida_data(data):
    try:
        # Tenta criar um objeto datetime a partir da string fornecida
        datetime.strptime(data, '%d-%m-%Y')
        return data
    except ValueError:
       data = input("Data invalida. Tente novamente: ")
       data = valida_data(data)

def valida_stts_p(status):
    sts = ['em andamento', 'concluido', 'cancelado']

    if (status not in sts):
        status = input("Status invalido. Tente novamente: ").lower()
        status = valida_stts_p(status)

    return status

def valida_stts_t(status):
    sts = ['em andamento', 'concluida', 'pendente']

    if (status not in sts):
        status = input("Status invalido. Tente novamente: ").lower()
        status = valida_stts_p(status)

    return status

def valida_projeto(nome):
    projetos = buscar_all_projeto_n()
    projetos = retira_tup(projetos)

    if (nome in projetos) is False:
        nome = input("Projeto invalido. Tente novamente: ").lower()
        nome = valida_projeto(nome)

    return nome

def valida_tarefa(id):
    tarefas = buscar_all_tarefa_n()
    tarefas = retira_tup(tarefas)

    if (id in tarefas) is False:
        id = input("Tarefa invalida. Tente novamente: ").lower()
        id = valida_tarefa(id)

    return id

def valida_habilidade_membro(habilidade, membro):
    result = 0
    id_hab = buscar_habilidade_id(habilidade)
    id_memb = buscar_membro_id(membro)
    tup = (id_hab[0], id_memb[0])

    hab_memb = buscar_hab_memb_all()

    if (tup in hab_memb):
        print("o membro já possui essa habilidade. Tente novamente ")
        result = 1

    return result

def valida_membro_projeto(projeto,membro):
    result = 0
    id_proj = buscar_projeto_id(projeto)
    id_memb = buscar_membro_id(membro)
    tup = (id_proj[0], id_memb[0])

    proj_memb = buscar_proj_memb_all()

    if (tup in proj_memb):
        print("o membro já está nesse projeto. Tente novamente ")
        result = 1
    return result

def retira_tup(array):
    n_array =[]
    for item in array:
        n_array.append(item[0])

    return n_array

def ver_exist_membro(nome):
    membros = buscar_all_membro()
    membros = retira_tup(membros)

    if (nome in membros):
        nome = input("Membro já cadastrado. Tente novamente: ").lower()
        nome = ver_exist_membro(nome)

    return nome

def ver_exist_habilidade(nome):
    habilidades = buscar_all_habilidade()
    habilidades = retira_tup(habilidades)

    if (nome in habilidades):
        nome = input("Habilidade já cadastrada. Tente novamente: ").lower()
        nome = ver_exist_habilidade(nome)

    return nome

def ver_exist_projeto(nome):
    projetos = buscar_all_projeto_n()
    projetos = retira_tup(projetos)

    if (nome in projetos):
        nome = input("Projeto já cadastrado. Tente novamente: ").lower()
        nome = ver_exist_projeto(nome)

    return nome
