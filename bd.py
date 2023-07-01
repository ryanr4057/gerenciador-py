import sqlite3
from datetime import datetime

conn = sqlite3.connect(f'banco_de_dados.sqlite3')

conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

def cria_tabela_membro():
    c.execute('''CREATE TABLE membro (
                    id_membro INTEGER PRIMARY KEY,
                    nome TEXT,
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
                    id_habilid INTEGER,
                    id_membro INTEGER,
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
                    respons INTEGER,
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
                    respons TEXT,
                    proj_assoc INTEGER,
                    FOREIGN KEY (proj_assoc) REFERENCES projeto(id_proj)
                 )''')
    conn.commit()

def cria_tabela_proj_memb():
    c.execute('''CREATE TABLE membros_projeto (
                    id_proj INTEGER,
                    id_membro INTEGER,
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
                    id_proj INTEGER,
                    FOREIGN KEY (id_proj) REFERENCES projeto(id_proj)
                 )''')
    conn.commit()

def cria_tabela_relatorios():
    c.execute('''CREATE TABLE relatorio (
                    id_relat INTEGER PRIMARY KEY,
                    data_ger DATE,
                    tipo TEXT,
                    id_proj INTEGER,
                    FOREIGN KEY (id_proj) REFERENCES projeto(id_proj)
                 )''')
    conn.commit()

def inserir_membro(nome, funcao):
    c.execute("INSERT INTO membro (nome, funcao) VALUES (?, ?)", (nome, funcao))
    conn.commit()

def inserir_habilidade(nome):
    c.execute("INSERT INTO habilidade (nome) VALUES (?)", (nome,))
    conn.commit()

def inserir_habilidade_membro(id_habilidade, id_membro):
    c.execute("INSERT INTO membro_habilidade (id_habilid, id_membro) VALUES (?, ?)", (id_habilidade, id_membro))
    conn.commit()

def inserir_projeto(nome, descric, data_ini, data_term, status, respons):
    c.execute("INSERT INTO projeto (nome, descric, data_ini, data_term, status, respons) VALUES (?, ?,?, ?, ?, ?)", (nome, descric, data_ini, data_term, status, respons))
    conn.commit()

def inserir_tarefa(descric, data_ini, data_term, status, respons, proj_assoc):
    c.execute("INSERT INTO tarefa (descric, data_ini, data_term, status, respons, proj_assoc) VALUES (?, ?, ?, ?, ?, ?)", (descric, data_ini, data_term, status, respons, proj_assoc))
    conn.commit()

def inserir_membro_projeto(id_proj, id_membro):
    c.execute("INSERT INTO membros_projeto (id_proj, id_membro) VALUES (?, ?)", (id_proj, id_membro))
    conn.commit()

def inserir_documento(nome, descric, data_cri, versao, id_proj):
    c.execute("INSERT INTO documento (nome, descric, data_cri, versao, id_proj) VALUES (?, ?, ?, ?, ?)", (nome, descric, data_cri, versao, id_proj))
    conn.commit()

def inserir_relatorio(data_ger, tipo, id_proj):
    c.execute("INSERT INTO relatorio (data_ger, tipo, id_proj) VALUES (?, ?, ?)", (data_ger, tipo, id_proj))
    conn.commit()

def editar_projeto_status(id_proj, status):
    c.execute("UPDATE projeto SET status = ? WHERE id_proj = ?", (status, id_proj))
    conn.commit()

def editar_projeto_respons(id_proj, id_membro):
    c.execute("UPDATE projeto SET respons = ? WHERE id_proj = ?", (id_membro, id_proj))
    conn.commit()

def editar_tarefa_status(id_tarefa, status):
    c.execute("UPDATE tarefa SET status = ? WHERE id_taref = ?", (status, id_tarefa))
    conn.commit()

def editar_tarefa_respons(id_tarefa, id_membro):
    c.execute("UPDATE tarefa SET respons = ? WHERE id_taref = ?", (id_membro, id_tarefa))
    conn.commit()

def buscar_proj_status(status):
    c.execute("SELECT nome FROM projeto WHERE status = (?)", (status,))
    return c.fetchall()

def buscar_tarefas_concluidas(id_proj):
    c.execute("SELECT descric FROM tarefa WHERE proj_assoc = (?) AND status = 'concluida'", (id_proj,))
    return c.fetchall()

def buscar_membros_habil(habilidade):
    c.execute("SELECT membro.nome FROM membro join membro_habilidade on membro.id_membro = membro_habilidade.id_membro join habilidade on habilidade.id_habilid = membro_habilidade.id_habilid  WHERE habilidade.nome = (?)", (habilidade,))
    return c.fetchall()

def buscar_proj_documentos(nome_proj):
    c.execute("SELECT documento.nome FROM documento join projeto on documento.id_proj = projeto.id_proj WHERE projeto.nome = (?)", (nome_proj,))
    return c.fetchall()

def buscar_proj_atras(data_at):
    c.execute("SELECT nome FROM projeto WHERE data_term < (?) AND status = 'em andamento' ", (data_at,))
    return c.fetchall()

def buscar_projetos_membro(nome_membro):
    c.execute("SELECT projeto.nome FROM projeto join membros_projeto on projeto.id_proj = membros_projeto.id_proj join membro on membros_projeto.id_membro = membro.id_membro WHERE membro.nome = (?)", (nome_membro,))
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

# cria_banco()

# inserir_membro('jarrel', 'scrum master')
# inserir_membro('juan', 'zelador')
# inserir_membro('roberio', 'hacker')

# inserir_habilidade("sql")
# inserir_habilidade_membro(4,5)
# inserir_projeto('bot', 'automacao', '01-01-2021', '01-03-2021', 'em andamento', 1)

# inserir_membro_projeto(2,5)

# inserir_projeto('limpeza', 'gerenciamento de disco', '10-06-2023', '20-06-2023', 'concluido', 3)

# inserir_tarefa('invadir conta', '11-06-2023', '12-06-2023', 'concluida', 4, 2)

# inserir_tarefa('reuniao', '14-06-2023', '15-06-2023', 'concluida', 5, 2)

# inserir_documento('manifesto', 'scrum', '19-06-2023', '1.1', 1)

# inserir_relatorio('18-06-2023', 'diario', 1)

# print(buscar_proj_status('em andamento'))

# print(buscar_tarefas_concluidas(2))

# print(buscar_membros_habil('sql'))

# print(buscar_proj_documentos('bot'))

# data_atual = datetime.now().strftime('%d-%m-%Y')

# print(buscar_proj_atras(data_atual))

# print(buscar_projetos_membro('jarrel'))

# editar_projeto_status(2, 'concluido')

# editar_projeto_respons(1,3)
