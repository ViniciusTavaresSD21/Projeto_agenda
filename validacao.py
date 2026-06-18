import sqlite3

def validar(valores_autorizados, valor_a_ser_validado):
    if valor_a_ser_validado in valores_autorizados:
        return True
    else:
        False


def isdigit(number):
    try:
        int(number)
        return True
    except:
        return False
    

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
