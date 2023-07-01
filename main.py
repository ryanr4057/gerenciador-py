import func as f
import sqlite3
import time
from datetime import datetime
import os

def limpar_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Outros sistemas operacionais (por exemplo, Unix)
        os.system('clear')

def menu_cadastros(op):
    limpar_console()
    while True :
        print("CADASTROS")
        print("-------------------------")
        print("MENU")
        print("1- CRIAR PROJETO")
        print("2- CRIAR TAREFA")
        print("3- CADASTRAR MEMBRO")
        print("4- CADASTRAR HABILIDADE")
        print("5- ATRIBUIR HABILIDADE A MEMBRO")
        print("6- ATRIBUIR MEMBRO A PROJETO")
        print("7- ATRIBUIR DOCUMENTO")
        print("8- CRIAR RELATORIO")
        print("9- VOLTAR")
        op1 = input('')

        if int(op1) == 1:
            print("CRIAR PROJETO")
            nome = input('NOME:').lower()
            nome = f.ver_exist_projeto(nome)
            descric = input('DESCRIÇÃO:').lower()
            data_ini = input('DATA INICIAL: (dd-mm-yyyy)')
            data_ini = f.valida_data(data_ini)
            data_term = input('DATA DO TERMINO PREVISTO: (dd-mm-yyyy)')
            data_term = f.valida_data(data_term)
            status = input('STATUS: (em andamento, concluido, cancelado)').lower()
            status = f.valida_stts_p(status)
            respons = input('NOME DO RESPONSAVEL: ').lower()
            respons = f.valida_membro(respons)

            f.inserir_projeto(nome, descric, data_ini, data_term, status, respons)
            limpar_console()
            print('Projeto criado com sucesso')
            time.sleep(3)

        elif int(op1) == 2:
            print("CRIAR TAREFA")
            descric = input('DESCRIÇÃO:').lower()
            data_ini = input('DATA INICIAL: (dd-mm-yyyy)')
            data_ini = f.valida_data(data_ini)
            data_term = input('DATA DO TERMINO PREVISTO: (dd-mm-yyyy)')
            data_term = f.valida_data(data_term)
            status = input('STATUS: (em andamento, concluida, pendente)').lower()
            status = f.valida_stts_t(status)
            respons = input('NOME DO RESPONSAVEL: ').lower()
            respons = f.valida_membro(respons)
            proj_assoc = input('NOME DO PROJETO: ').lower()
            proj_assoc = f.valida_projeto(proj_assoc)

            f.inserir_tarefa(descric, data_ini, data_term, status, respons, proj_assoc)
            limpar_console()
            print('Tarefa criada com sucesso')
            time.sleep(3)

        elif int(op1) == 3:
            print("CADASTRAR MEMBRO")
            nome = input('NOME: ').lower()
            nome = f.ver_exist_membro(nome)
            funcao = input('FUNÇÃO: ').lower()

            f.inserir_membro(nome, funcao)
            limpar_console()
            print('Membro cadastrado com sucesso')
            time.sleep(3)

        elif int(op1) == 4:
            print("CADASTRAR HABILIDADE")
            nome = input('NOME DA HABILIDADE: ').lower()
            nome = f.ver_exist_habilidade(nome)
            f.inserir_habilidade(nome)
            limpar_console()
            print('Habilidade cadastrada com sucesso')
            time.sleep(3)

        elif int(op1) == 5:
            print("ATRIBUIR HABILIDADE A MEMBRO")
            nome_m = input('NOME DO MEMBRO: ').lower()
            nome_m = f.valida_membro(nome_m)
            nome_h = input('NOME DA HABILIDADE: ').lower()
            nome_h = f.valida_habilidade(nome_h)

            if (f.valida_habilidade_membro(nome_h, nome_m) == 0):
                f.inserir_habilidade_membro(nome_m, nome_h)
                limpar_console()
                print('Habilidade atribuida com sucesso')
                time.sleep(3)

        elif int(op1) == 6:
            print("ATRIBUIR MEMBRO A PROJETO")
            nome_m = input('NOME DO MEMBRO: ').lower()
            nome_m = f.valida_membro(nome_m)
            nome_p = input('NOME DO PROJETO: ').lower()
            nome_p = f.valida_projeto(nome_p)

            if (f.valida_membro_projeto(nome_p, nome_m) == 0):
                f.inserir_membro_projeto(nome_p, nome_m)
                limpar_console()
                print('Projeto atribuido com sucesso')
                time.sleep(3)

        elif int(op1) == 7:
            print("ATRIBUIR DOCUMENTO")
            nome = input('NOME: ').lower()
            desc = input('DESCRIÇÃO: ').lower()
            data_cri = input('DATA DE CRIAÇÃO: (dd-mm-yyyy) ').lower()
            data_cri = f.valida_data(data_cri)
            versao = input('VERSÃO: ').lower()
            nome_p = input('NOME DO PROJETO: ').lower()
            nome_p = f.valida_projeto(nome_p)

            f.inserir_documento(nome, desc, data_cri, versao, nome_p)
            limpar_console()
            print('Documento atribuido com sucesso')
            time.sleep(3)

        elif int(op1) == 8:
            print("CRIAR RELATORIO")
            data_cri = input('DATA DE CRIAÇÃO: (dd-mm-yyyy) ').lower()
            tipo = input('TIPO: ').lower()
            nome_p = input('NOME DO PROJETO: ').lower()
            nome_p = f.valida_projeto(nome_p)

            f.inserir_relatorio(nome, tipo, nome_p)
            limpar_console()
            print('Relatorio atribuido com sucesso')
            time.sleep(3)

        elif int(op1) == 9:
            limpar_console()
            break

        else:
            op = input("Opção inválida, tente novamente:")
            menu_cadastros(op)

def menu_buscas(op):
    limpar_console()
    while True :
        print("BUSCAS")
        print("-------------------------")
        print("MENU")
        print("1- BUSCAR TODOS OS PROJETOS")
        print("2- BUSCAR TODOS OS MEMBROS")
        print("3- BUSCAR TODAS AS HABILIDADES")
        print("4- BUSCAR TODAS AS TAREFAS")
        print("5- BUSCAR MEMBROS COM UMA HABILIDADE")
        print("6- BUSCAR PROJETOS DE UM MEMBRO")
        print("7- BUSCAR MEMBROS DE UM PROJETO")
        print("8- BUSCAR DOCUMENTOS DE UM PROJETO")
        print("9- BUSCAR PROJETOS POR STATUS")
        print("10- BUSCAR TAREFAS CONCLUIDAS DE UM PROJETO")
        print("11- BUSCAR PROJETOS ATRASADOS")
        print("12- BUSCAR TAREFAS DE UM PROJETO")
        print("13- BUSCAR RELATORIOS DE UM PROJETO")
        print("14- VOLTAR")
        op1 = input(' ')

        if int(op1) == 1:
            limpar_console()
            projs = f.buscar_all_projeto()
            for proj in projs:
                print(f'NOME DO PROJETO: {proj[0]}           RESPONSÁVEL: {proj[1]}')

            time.sleep(5)

        elif int(op1) == 2:
            limpar_console()
            projs = f.buscar_all_membro()
            for proj in projs:
                print(f'NOME: {proj[0]}  FUNÇÃO: {proj[1]}')
            time.sleep(5)

        elif int(op1) == 3:
            limpar_console()
            projs = f.buscar_all_habilidade()
            for proj in projs:
                print(f'{proj[0]}')

            time.sleep(5)

        elif int(op1) == 4:
            limpar_console()
            projs = f.buscar_all_tarefa()
            for proj in projs:
                print(f'DESCRIÇÃO:{proj[0]},    RESPONSÁVEL: {proj[1]},    PROJETO: {proj[2]}')

            time.sleep(5)

        elif int(op1) == 5:
            limpar_console()
            hab = input('HABILIDADE: ').lower()
            hab = f.valida_habilidade(hab)
            limpar_console()
            print(f"MEMBROS COM A HABILIDADE: {hab}")
            projs = f.buscar_membros_habil(hab)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 6:
            limpar_console()
            memb = input('MEMBRO: ').lower()
            memb = f.valida_membro(memb)
            limpar_console()
            print(f'PROJETOS DO MEMBRO: {memb}')
            projs = f.buscar_projetos_membro(memb)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 7:
            limpar_console()
            proje = input('PROJETO: ').lower()
            proje = f.valida_projeto(proje)
            limpar_console()
            print(f'MEMBROS DO PROJETO: {proje}')
            projs = f.buscar_membros_projeto(proje)
            for proj in projs:
                # print(proj)
                print(f'NOME: {proj[0]}  FUNÇÃO: {proj[1]}')
            time.sleep(5)

        elif int(op1) == 8:
            limpar_console()
            proje = input('PROJETO: ').lower()
            proje = f.valida_projeto(proje)
            limpar_console()
            print(f'DOCUMENTOS DO PROJETO: {proje}')
            projs = f.buscar_proj_documentos(proje)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 9:
            limpar_console()
            stss = input('STATUS (em andamento, concluido, cancelado): ').lower()
            stss = f.valida_stts_p(stss)
            limpar_console()
            print(f'PROJETOS COM O STATUS: {stss}')
            projs = f.buscar_proj_status(stss)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 10:
            limpar_console()
            stss = input('PROJETO: ').lower()
            stss = f.valida_projeto(stss)
            limpar_console()
            print(f'TAREFAS CONCLUIDAS DO PROJETO: {stss}')
            projs = f.buscar_tarefas_concluidas(stss)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 11:
            limpar_console()
            print('PROJETOS ATRASADOS:')
            projs = f.buscar_proj_atras()
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 12:
            limpar_console()
            stss = input('PROJETO: ').lower()
            stss = f.valida_projeto(stss)
            print(f'TAREFAS DO PROJETO: {stss}')
            projs = f.buscar_tarefas_proj(stss)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 13:
            limpar_console()
            proje = input('PROJETO: ').lower()
            proje = f.valida_projeto(proje)
            limpar_console()
            print(f'RELATORIOS DO PROJETO: {proje}')
            projs = f.buscar_proj_relatorios(proje)
            for proj in projs:
                print(f'{proj[0]}')
            time.sleep(5)

        elif int(op1) == 14:
            limpar_console()
            break

        else:
            op = input("Opção inválida, tente novamente:")
            menu_buscas(op)

def menu_editar(op):
    limpar_console()
    while True :
        print("EDITAR STATUS DE PROJETOS / TAREFAS")
        print("-------------------------")
        print("MENU")
        print("1- EDITAR STATUS DE UM PROJETO")
        print("2- EDITAR STATUS DE UMA TAREFA")
        print("3- EDITAR RESPONSAVEL DE UM PROJETO")
        print("4- EDITAR RESPONSAVEL DE UMA TAREFA")
        print("5- PRAZO DE UM PROJETO")
        print("6- PRAZO DE UMA TAREFA")
        print("7- VOLTAR")
        op1 = input(' ')

        if int(op1) == 1:
            limpar_console()
            proj = input('PROJETO: ').lower()
            proj = f.valida_projeto(proj)
            stts = input('STATUS (em andamento, concluido, cancelado): ').lower()
            stts - f.valida_stts_p(stts)

            f.editar_projeto_status(proj, stts)
            limpar_console()
            print('Status atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 2:
            limpar_console()
            proj = int(input('ID TAREFA: '))
            proj = f.valida_projeto(proj)
            stts = input('STATUS (em andamento, concluida, pendente): ').lower()
            stts - f.valida_stts_t(stts)

            f.editar_tarefa_status(proj, stts)
            limpar_console()
            print('Status atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 3:
            limpar_console()
            proj = input('PROJETO: ').lower()
            proj = f.valida_projeto(proj)
            resp = input('RESPONSÁVEL: ').lower()
            resp = f.valida_membro(resp)

            f.editar_projeto_respons(proj, resp)
            limpar_console()
            print('Responsavel atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 4:
            limpar_console()
            proj = int(input('ID TAREFA: '))
            proj = f.valida_tarefa(proj)
            resp = input('RESPONSÁVEL: ').lower()
            resp = f.valida_membro(resp)

            f.editar_tarefa_respons(proj, stts)
            limpar_console()
            print('Responsavel atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 5:
            limpar_console()
            projeto = input('PROJETO: ').lower()
            projeto = f.valida_projeto(projeto)
            data_term = input('DATA DO TERMINO PREVISTO: (dd-mm-yyyy)')
            data_term = f.valida_data(data_term)

            f.editar_projeto_prazo(projeto, data_term)
            limpar_console()
            print('Prazo atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 6:
            limpar_console()
            tarefa = int(input('ID TAREFA: '))
            tarefa = f.valida_tarefa(tarefa)
            data_term = input('DATA DO TERMINO PREVISTO: (dd-mm-yyyy)').lower()
            data_term = f.valida_data(data_term)

            f.editar_tarefa_prazo(tarefa, data_term)
            limpar_console()
            print('Prazo atualizado com sucesso')
            time.sleep(3)

        elif int(op1) == 7:
            limpar_console()
            break

        else:
            op = input("Opção inválida, tente novamente:")
            menu_editar(op)

while True:
    print("GERENCIAMENTO DE PROJETOS")
    print("-------------------------")
    print("MENU")
    print("1- CRIAÇÃO / CADASTROS")
    print("2- BUSCAS")
    print("3- EDITAR STATUS DE PROJETOS / TAREFAS")
    print("4- SAIR")

    op = input(' ')

    if int(op) == 1:
        menu_cadastros(op)
    elif int(op) == 2:
        menu_buscas(op)
    elif int(op) == 3:
        menu_editar(op)
    elif int(op) == 4:
        break


