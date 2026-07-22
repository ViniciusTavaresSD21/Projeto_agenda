import sqlite3
import questionary
import sys
from time import sleep
from os import system
sys.path.append('/Users/vinicius/Documents/GitHub/Projeto_agenda')

from validacao import validar_nome_tabela
from formatacao_e_menu import menu_texto, linha_menu, marcar_textos
from funcoes.atividade import menu_atividade

conexao = sqlite3.connect("projetos.db")


class Projeto:
    """
    Cria, deleta e renomeia tabelas com colunas prontas para receber atividades.
    """

    def __init__(self, nome_da_pasta="Sem_titulo"):
        self._nome_da_pasta = nome_da_pasta

    def criar_projeto(self):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self._nome_da_pasta} (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL, prazo TEXT NOT NULL, status TEXT NOT NULL)"""
            )
        conexao.commit()

    def deletar_projeto(self):
        try:
            with sqlite3.connect("projetos.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(f"DROP TABLE {self._nome_da_pasta}")
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")

    def renomear_projeto(self, novo_nome):
        try:
            with sqlite3.connect("projetos.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    f"""ALTER TABLE {self._nome_da_pasta} RENAME TO {novo_nome}"""
                )
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")
            sleep(10)

    def ver_todos_os_projetos(self):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name""")
            tabela = [linha[0] for linha in cursor.fetchall()]
        return tabela


estilo = questionary.Style(
    [
        ("question", "fg:cyan bold"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:cyan"),
        ("", "fg:green"),
    ]
)


def menu_projeto():
    while True:
        system("cls")
        menu_texto(
            "PROJETOS",
            tamanho=65,
            cor="azul",
            cor_texto="verde",
            negrito=True,
            negrito_texto=True,
        )
        opcao = questionary.select(
            "",
            choices=[
                "Criar Projeto",
                "Deletar Projeto",
                "Renomear Projeto",
                "Meus Projetos",
                "Sair",
            ],
            qmark="",
            instruction="Use as setas do teclado",
            style=estilo,
        ).ask()
        linha_menu(tamanho=65, cor="azul", negrito=True)

        if opcao == "Criar Projeto":
            while True:
                nome = str(
                    questionary.text("Nome do projeto: ", qmark="", style=estilo).ask()
                )
                if nome.lower() == "sair":
                    break

                elif validar_nome_tabela(nome) == True:
                    Projeto(nome).criar_projeto()
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(marcar_textos("Projeto criado.", "verde", True))
                    sleep(2)
                    break
                else:
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(
                        marcar_textos(
                            "Já existe um projeto com esse nome.", "vermelho", True
                        )
                    )
                    sleep(2)
                    system("cls")

        elif opcao == "Deletar Projeto":
            while True:
                lista_nomes_projeto = Projeto().ver_todos_os_projetos()
                lista_nomes_projeto.append("Sair")
                nome = questionary.select(
                    "Selecione o projeto:",
                    lista_nomes_projeto,
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()

                if nome.lower() == "sair":
                    break

                else:
                    Projeto(nome).deletar_projeto()
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos(
                            f"O projeto '{nome}' foi deletado.", "verde", True
                        )
                    )
                    sleep(2)
                    break

        elif opcao == "Renomear Projeto":
            while True:
                system("cls")
                menu_texto(
                    "Renomeando projeto",
                    tamanho=65,
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )
                lista_nomes_projeto = Projeto().ver_todos_os_projetos()
                lista_nomes_projeto.append("Sair")
                nome = questionary.select(
                    "Selecione o projeto que vai ser renomeado:",
                    lista_nomes_projeto,
                    instruction=" ",
                    style=estilo,
                    qmark="",
                ).ask()

                if nome.lower() == "sair":
                    break

                else:
                    while True:
                        system("cls")
                        menu_texto(
                            "Renomeando projeto",
                            tamanho=65,
                            cor="azul",
                            cor_texto="verde",
                            negrito=True,
                            negrito_texto=True,
                        )
                        novo_nome = str(
                            questionary.text(
                                "Novo nome do projeto: ", qmark="", style=estilo
                            ).ask()
                        )

                        if novo_nome.lower() == "sair":
                            break

                        with sqlite3.connect("projetos.db") as conexao:
                            cursor = conexao.cursor()
                            cursor.execute(
                                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                                (novo_nome,)
                            )
                            if cursor.fetchone():
                                linha_menu(tamanho=65, cor="azul", negrito=True)
                                print(marcar_textos(f"ERRO: A tabela '{novo_nome}' já existe!", "amarelo", True))
                                sleep(2)
                                system('cls')

                            else:
                                Projeto(nome).renomear_projeto(novo_nome)
                                linha_menu(tamanho=65, cor="azul", negrito=True)
                                print(marcar_textos("Processando...", "amarelo", True))
                                sleep(2)
                                print(
                                    marcar_textos(
                                        f'O projeto "{nome}" foi renomeado para "{novo_nome}.',
                                        "verde",
                                        True,
                                    )
                                )
                                sleep(2)
                                break
                break
                   

        elif opcao == "Meus Projetos":
            while True:
                system('cls')
                menu_texto("MEUS PROJETOS", cor="azul", cor_texto="verde", )
                lista_de_projetos = Projeto().ver_todos_os_projetos()
                lista_de_projetos.append("Sair")
                projeto_selecionado = questionary.select("Escolha um projeto: ", lista_de_projetos, qmark="", instruction=" ", style=estilo).ask()
                if projeto_selecionado == "Sair":
                    break

                menu_atividade(projeto_selecionado)
                break

        elif opcao == "Sair":
            break