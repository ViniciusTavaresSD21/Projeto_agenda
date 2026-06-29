import sqlite3
from datetime import date


def validar(valores_autorizados, valor_a_ser_validado):
    if valor_a_ser_validado in valores_autorizados:
        return True
    else:
        False


def validar_nome_tabela(nome_do_projeto):
    try:
        with sqlite3.connect('registros_diarios.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name""")
            tabela = [linha[0] for linha in cursor.fetchall()]

        if nome_do_projeto not in tabela:
            return True
        else:
            return False
    except Exception as erro:
        print(f"ERRO: {erro}")
        return


def validar_titulo_atividade(pasta_do_projeto, titulo_da_atividade):
    try:
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            titulos = cursor.execute(f"""SELECT titulo from {pasta_do_projeto}""").fetchall()
        if titulo_da_atividade in titulos:
            True
        else:
            return False
    except Exception as erro:
        print(f"ERRO: {erro}")


def validar_formato_data(data):
    try:
        if len(data) != 10 or data.count('/') != 2:
            return False
        termos = data.split('/')

        for item in termos:
            if item.isdigit() == False:
                return False
            
        if int(termos[0]) > 31:
            return False
        
        elif int(termos[1]) > 12:
            return False
        else:
            return True
    except:
        return False


def validar_tempo_da_data(data, anterior_ou_posterior="posterior"):
    data_objeto = date.strptime(data, "%d/%m/%Y")
    if anterior_ou_posterior == "posterior":
        if data_objeto >= date.today():
            return True
        else:
            return False
    elif anterior_ou_posterior == "anterior":
        if data_objeto <= date.today():
            return True
        else:
            return False
    