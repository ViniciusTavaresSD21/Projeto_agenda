import sqlite3
import questionary
import sys

from time import sleep
from datetime import date, datetime
from os import system
from textwrap import fill
from formatacao_e_menu import linha_menu, menu_texto, marcar_textos

sys.path.append('/Users/vinicius/Documents/GitHub/Projeto_agenda')

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
                    print(f"{marcar_textos("Data do registro:", "azul", True)} {marcar_textos(registro["data"], "amarelo")}")
                    print()
                    print(f"{marcar_textos("Registro:", "azul", True)}")
                    print(f"{marcar_textos(fill(registro["registro"], 50), "verde", True)}")
                    linha_menu(tamanho=60, cor="azul", negrito=True)
        except Exception as erro:
            print(f"ERRO: {erro}")


estilo = questionary.Style(
    [
        ("question", "fg:cyan bold"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:cyan"),
        ("", "fg:green"),
    ]
)


def menu_agenda():
    while True:
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
            choices=["Adicionar registro", "Deletar", "editar", "Meus registros", "Sair"],
            qmark="",
            instruction="Use as setas do teclado.",
            style=estilo,
        ).ask()

        if opcao == "Adicionar registro":
            while True:
                system("cls")
                menu_texto(
                    "Adicionando registro",
                    tamanho=60,
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )

                data = questionary.text(
                    "Em qual data você deseja fazer o registro?",
                    qmark="",
                    instruction="", 
                    style=estilo
                ).ask()

                if data.lower() == "sair":
                    break
                
                try:
                    datetime.strptime(data, "%d/%m/%Y")
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    anotacao = questionary.text(
                        "Digite:", qmark="", instruction="", style=estilo
                    ).ask()
                    if anotacao.lower() == "sair":
                        break

                    Agenda(anotacao, data).registrar()
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos("Registro adicionado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    system("cls")
                    break

                except:
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(marcar_textos("Digite a data no formato (dia/mês/ano).", "amarelo", True))
                    sleep(2)
                    system("cls")

        elif opcao == "Deletar":
            while True:
                system('cls')
                menu_texto(
                    "Deletando registros",
                    tamanho=60,
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )
                lista_de_registros = Agenda().todos_os_registros()
                lista_de_registros.append("Sair")
                registro = questionary.select(
                    "Qual registro você deseja deletar?",
                    lista_de_registros,
                    qmark="",
                    instruction=" ",
                    style=estilo
                ).ask()

                if registro.lower() == "sair":
                    break

                else:
                    Agenda().deletar(registro)
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos("Registro deletado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    system("cls")
                    break

        elif opcao == "editar":
            while True:
                system('cls')
                menu_texto(
                    "Editando Registros",
                    tamanho=60,
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )
                linha_menu(tamanho=60, cor="azul", negrito=True)
                lista_de_registros = Agenda().todos_os_registros()
                lista_de_registros.append("Sair")
                registro = questionary.select(
                    "Qual registro você deseja editar?",
                    lista_de_registros,
                    qmark="",
                    instruction=" ",
                    style=estilo
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
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(marcar_textos("Registro editado com sucesso.", "verde", True))
                    sleep(2)
                    system("cls")
                    break

        elif opcao == "Meus registros":
            while True:
                system('cls')
                menu_texto(
                    "Meus registros",
                    tamanho=60,
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )
                Agenda().visualizar_todos()
                input(marcar_textos("Aperte enter para sair", "preto"))
                system("cls")
                break

        elif opcao == "Sair":
            break
