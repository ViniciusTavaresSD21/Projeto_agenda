import sqlite3
from time import sleep
from datetime import date
from os import system
import questionary
import sys
sys.path.append('/Users/vinicius/Documents/GitHub/Projeto_agenda')
from validacao import validar_formato_data
from formatacao_e_menu import linha_menu, menu_texto, marcar_textos


conexao = sqlite3.connect("agenda.db")

with sqlite3.connect("agenda.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
    """)


class Agenda:
    # """Esse classe representa um registro de um texto"""
    def __init__(self, texto="", data=date.today()):
        self._texto = texto
        self._data_hora = data

    def registrar(self):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "INSERT INTO Diario (registro, data) VALUES (?, ?)",
                    (self._texto, self._data_hora),
                )
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")

    def deletar(self, registro):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("""DELETE FROM Diario WHERE registro = ?""", (registro,))
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")

    def ler_registro(self, id):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                cursor = conexao.cursor()
                linha = cursor.execute(
                    f"SELECT * FROM Diario WHERE id = {id}"
                ).fetchone()
                return linha
        except Exception as erro:
            print(f"ERRO: {erro}")

    def editar(self, registro):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    "UPDATE Diario SET registro = ? WHERE registro = ?;",
                    (self._texto, registro),
                )
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")

    def todos_os_registros(self):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("""SELECT registro FROM Diario;""")
                ids = [linha[0] for linha in cursor.fetchall()]
                return ids
        except Exception as erro:
            print(f"ERRO: {erro}")

    def visualizar_todos(self):
        try:
            with sqlite3.connect("agenda.db") as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()
                cursor.execute("""SELECT * FROM Diario;""")
                registros = cursor.fetchall()
                linha_menu(tamanho=60, cor="azul", negrito=True)
                for registro in registros:
                    print(f"Data do registro: {registro["data"]}")
                    print()
                    print(f"{registro["registro"]}")
                linha_menu(tamanho=60, cor="azul", negrito=True)
        except Exception as erro:
            print(f"ERRO: {erro}")


estilo = questionary.Style(
    [
        ("question", "fg:red"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:red"),
        ("", "fg:green"),
    ]
)


def menu_agenda():
    while True:
        conexao
        system("cls")
        menu_texto(
            "AGENDA",
            tamanho=60,
            cor="azul",
            cor_texto="verde",
            negrito=True,
            negrito_texto=True,
        )
        opcao = questionary.select(
            "",
            choices=["Adicionar registro", "Deletar", "editar", "Ver todos", "Sair"],
            qmark="",
            instruction="Use as setas do teclado.",
            style=estilo,
        ).ask()

        if opcao == "Adicionar registro":
            while True:
                linha_menu(tamanho=60, cor="azul", negrito=True)
                data = questionary.text(
                    "Em qual data você deseja fazer um registro?",
                    qmark=" ",
                    instruction="",
                ).ask()
                if data.lower() == "sair":
                    break

                elif validar_formato_data(data) == True:

                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    anotacao = questionary.text(
                        "Digite:", qmark="", instruction=""
                    ).ask()
                    Agenda(anotacao, data).registrar()
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print("Processando...")
                    sleep(2)
                    print(
                        marcar_textos("Registro adicionado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    system("cls")
                    break
                else:
                    print("Digite no formato (dia/mês/ano)")
                    sleep(2)
                    system("cls")

        elif opcao == "Deletar":
            while True:
                linha_menu(tamanho=60, cor="azul", negrito=True)
                lista_de_registros = Agenda().todos_os_registros()
                lista_de_registros.append("Sair")
                registro = questionary.select(
                    "Qual registro você deseja deletar?",
                    lista_de_registros,
                    qmark="",
                    instruction=" ",
                ).ask()
                if registro.lower() == "sair":
                    break

                else:
                    Agenda().deletar(registro)
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print("Processando...")
                    sleep(2)
                    print(
                        marcar_textos("Registro deletado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    system("cls")
                    break

        elif opcao == "editar":
            while True:
                linha_menu(tamanho=60, cor="azul", negrito=True)
                lista_de_registros = Agenda().todos_os_registros()
                lista_de_registros.append("Sair")
                registro = questionary.select(
                    "Qual registro você deseja editar?",
                    lista_de_registros,
                    qmark="",
                    instruction=" ",
                ).ask()
                if registro.lower() == "sair":
                    break

                else:
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    novo_texto = input("Escreva o novo texto: ")
                    if novo_texto == "sair":
                        break

                    Agenda(novo_texto).editar(registro)
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print("Processando...")
                    sleep(2)
                    print(marcar_textos("Registro editado com sucesso.", "verde", True))
                    sleep(2)
                    system("cls")
                    break

        elif opcao == "Ver todos":
            while True:
                Agenda().visualizar_todos()
                input("Aperte enter para sair.")
                system("cls")
                break

        elif opcao == "Sair":
            linha_menu(tamanho=60, cor="azul", negrito=True)
            print("Encerrando...")
            sleep(2)
            print(marcar_textos("Programa encerrado.", "amarelo", True))
            break


menu_agenda()
