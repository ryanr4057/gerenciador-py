import sqlite3
from datetime import datetime

conn = sqlite3.connect(f'banco_de_dados.sqlite3')

conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

def inserir_habilidade_membro(id_habilidade, id_membro):
    c.execute("INSERT INTO membro_habilidade (id_habilid, id_membro) VALUES (?, ?)", (id_habilidade, id_membro))
    conn.commit()

def buscar_projetos_membro(nome_membro):
    c.execute("SELECT projeto.nome FROM projeto join membros_projeto on projeto.id_proj = membros_projeto.id_proj join membro on membros_projeto.id_membro = membro.id_membro WHERE membro.nome = (?)", (nome_membro,))
    return c.fetchall()
