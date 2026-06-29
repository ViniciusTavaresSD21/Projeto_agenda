import sqlite3
import questionary
from time import sleep
from os import system
from validacao import validar_nome_tabela
from formatacao_e_menu import menu_texto, linha_menu, marcar_textos

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
        ("question", "fg:red"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:red"),
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
                "Ver todos",
                "Sair",
            ],
            qmark="",
            instruction="Use as setas do teclado",
            style=estilo,
        ).ask()
        linha_menu(tamanho=65, cor="azul", negrito=True)

        if opcao == "Criar Projeto":
            while True:
                print(
                    marcar_textos("Digite 'sair' para voltar pro menu.", "preto", None)
                )
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
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
                )
                lista_nomes_projeto = Projeto().ver_todos_os_projetos()
                lista_nomes_projeto.append("Sair")
                nome = questionary.select(
                    "Selecione o projeto:",
                    lista_nomes_projeto,
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()

                if nome.lower() == "Sair":
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
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
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
                    novo_nome = str(
                        questionary.text(
                            "Novo nome do projeto: ", qmark="", style=estilo
                        ).ask()
                    )
                    if novo_nome.lower() == "sair":
                        break

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

        elif opcao == "Ver todos":
            while True:
                lista_de_projetos = Projeto().ver_todos_os_projetos()
                for projeto in lista_de_projetos:
                    print(f"*{marcar_textos(projeto, "verde", True)}")
                linha_menu(tamanho=65, cor="azul", negrito=True)
                print(marcar_textos("Aperte enter para sair.", "preto"))
                input()
                break

        elif opcao == "Sair":
            break
