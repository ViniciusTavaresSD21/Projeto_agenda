import sqlite3

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
    if len(data) != 10 or data.count('/') != 2:
        return
    termos = data.split('/')
    for item in termos:
        if item.isdigit() == False:
            break
    else:
        return True