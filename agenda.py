import sqlite3
from time import sleep
from datetime import datetime
from os import system
import questionary
from formatacao_e_menu import menu_texto, linha_menu, marcar_textos, visualizar_toda_agenda
from validacao import isdigit


conexao = sqlite3.connect('registros_diarios.db')
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
""")

def verificar_id(numero_do_id):
    cursor.execute("""SELECT id FROM Diario;""")
    ids = cursor.fetchall()
    for id in ids:
        if id["id"] == numero_do_id:
            return True


class Registro:
    #"""Esse classe representa um registro de um texto"""
    def __init__(self, texto=''):
        self._texto = texto
        self._data_hora = datetime.now().strftime("%d/%m/%Y ás %H:%M")
    
    def registrar(self):
        cursor.execute("INSERT INTO Diario (registro, data) VALUES (?, ?)", (self._texto, self._data_hora))
        conexao.commit()
    
    def deletar(self, id):
        cursor.execute("""DELETE FROM Diario WHERE id = ?""", (id,))
        conexao.commit()
    
    def ler_registro(self, id):
        linha = cursor.execute(f"SELECT * FROM Diario WHERE id = {id}").fetchone()
        return linha
        
    def editar(self, id):
        cursor.execute("UPDATE Diario SET registro = ? WHERE id = ?;", (self._texto, id) )
        conexao.commit()
  

    def ver_todos(self):
        cursor.execute("SELECT * FROM Diario")
        todos_os_registros = cursor.fetchall()
        return todos_os_registros
    
estilo = questionary.Style([
    ('question', 'fg:red'),
    ('highlighted', 'fg:yellow bold'),
    ('instruction', 'fg:gray'),
    ('pointer', 'fg:red'),
    ('', 'fg:green')
    ])


def agenda():
    while True:
        conexao
        system('cls')
        menu_texto("AGENDA", tamanho=50, cor="azul", cor_texto="verde", negrito=True, negrito_texto=True)
        opcao = questionary.select("", choices=["Adicionar registro", "Deletar", "editar", "Ver todos", "Sair"], qmark="", instruction="Use as setas do teclado.", style=estilo).ask()
        if opcao == "Adicionar registro":
            linha_menu(tamanho=50, cor="azul", negrito=True)
            print("Fale um pouco sobre o seu dia...")
            print()
            texto = input()
            Registro(texto).registrar()
            linha_menu(tamanho=50, cor="azul", negrito=True)
            print("Processando...")
            sleep(2)
            print(marcar_textos("Registro adicionado com sucesso.", "verde", True))
            sleep(2)
            system('cls')

        elif opcao == "Deletar":
            linha_menu(tamanho=50, cor="azul", negrito=True)
            numero_do_id = int(questionary.text("Qual o ID do registro que você deseja deletar? ", validate=isdigit, qmark="").ask())
            if verificar_id(numero_do_id) == True:
                Registro().deletar(numero_do_id)
                linha_menu(tamanho=50, cor="azul", negrito=True)
                print("Processando...")
                sleep(2)
                print(marcar_textos("Registro deletado com sucesso.", "verde", True))
                sleep(2)
                system('cls')
            else:
                linha_menu(tamanho=50, cor="azul", negrito=True)
                print(marcar_textos("Não há nenhum registro com esse ID.", "vermelho", True))
                sleep(2)
                system('cls')

        elif opcao == "editar":
            linha_menu(tamanho=50, cor="azul", negrito=True)
            numero_do_id = int(questionary.text("Qual o ID do registro que você deseja editar? ", validate=isdigit, qmark="").ask())
            if verificar_id(numero_do_id) == True:
                novo_texto = input("Escreva o novo texto: ")
                Registro(novo_texto).editar(numero_do_id)
                linha_menu(tamanho=50, cor="azul", negrito=True)
                print("Processando...")
                sleep(2)
                print(marcar_textos("Registro editado com sucesso.", "verde", True))
                sleep(2)
                system('cls')
            else:
                linha_menu(tamanho=50, cor="azul", negrito=True)
                print(marcar_textos("Não há nenhum registro com esse ID.", "vermelho", True))
                sleep(2)
                system('cls')

        elif opcao == "Ver todos":
            while True:
                tabela = cursor.execute("""SELECT * FROM Diario""").fetchall()
                visualizar_toda_agenda(tabela)
                questionary.text("Aperte enter para sair.", "", None, "").ask()
                system('cls')
                break

        elif opcao == "Sair":
            linha_menu(tamanho=50, cor="azul", negrito=True)
            print("Encerrando...")
            sleep(2)
            print(marcar_textos("Programa encerrado.", "amarelo", True))
            break
agenda()