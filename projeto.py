import sqlite3
import questionary
from time import sleep
from os import system
from validacao import validar_nome_tabela
from formatacao_e_menu import menu_texto, linha_menu, marcar_textos

conexao = sqlite3.connect("registros_diarios.db")
conexao.row_factory = sqlite3.Row

with sqlite3.connect("registros_diarios.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
    """)
    conexao.commit()


class Projeto:
    '''
    Cria, deleta e renomeia tabelas com colunas prontas para receber atividades.
    '''
    def __init__(self, nome_da_pasta):
        self._nome_da_pasta = nome_da_pasta


    def criar_projeto(self):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor(
            f"""CREATE TABLE IF NOT EXISTS {self._nome_da_pasta} (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL, prazo TEXT NOT NULL, status TEXT NOT NULL)"""
        )
        conexao.commit()


    def deletar_projeto(self):
        try:
            with sqlite3.connect("registros_diarios.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("BEGIN TRANSACTION")
                cursor.execute(f"DROP TABLE {self._nome_da_pasta}")
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")

    def renomear_projeto(self, novo_nome):
        try:
            with sqlite3.connect("registros_diarios.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(f"""ALTER TABLE {self._nome_da_pasta} RENAME TO {novo_nome}""")
                conexao.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")


class Atividade:
    def __init__(self, nome_da_pasta, titulo="Sem titulo", descricao="", prazo=None):
        self._titulo = titulo
        self._descricao = descricao
        self._prazo = prazo
        self._status = "Não concluído"
        self._nome_da_pasta = nome_da_pasta

    def criar(self, prazo):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"INSERT INTO {self._nome_da_pasta} (titulo, descricao, prazo, status) VALUES (?, ?, ?, ?)",
            (self._titulo, self._descricao, prazo, self._status),
        )
        conexao.commit()

    def deletar(self, id):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"""DELETE FROM {self._nome_da_pasta} WHERE id = ?""", (id,)
        )
        conexao.commit()

    def ler_atividade(self, id):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            linha = cursor.execute(
            f"SELECT * FROM {self._nome_da_pasta} WHERE id = {id}"
        ).fetchone()
        conexao.close()
        return linha

    def editar_titulo(self, id):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"UPDATE {self._nome_da_pasta} SET titulo = ? WHERE id = ?;",
            (self._titulo, id),
        )
        conexao.commit()

    def editar_descricao(self, id):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"UPDATE {self._nome_da_pasta} SET descricao = ? WHERE id = ?;",
            (self._descricao, id),
        )
        conexao.commit()

    def editar_prazo(self, id):
        with sqlite3.connect("registros_diarios.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"UPDATE {self._nome_da_pasta} SET prazo = ? WHERE id = ?;",
            (self._prazo, id),
        )
        conexao.commit()


estilo = questionary.Style(
    [
        ("question", "fg:red"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:red"),
        ("", "fg:green"),
    ]
)


def projeto():
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
            choices=["Criar Projeto", "Deletar Projeto", "Renomear Projeto", "Ver todos", "Sair"],
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
                if nome == "sair":
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
                    marcar_textos("Digite 'sair' para voltar pro menu.", "preto", None)
                )
                nome = str(
                    questionary.text("Nome do projeto: ", qmark="", style=estilo).ask()
                )
                if nome == "sair":
                    break
                elif validar_nome_tabela(nome) == False:
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
                else:
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(
                        marcar_textos(
                            "Não existe um projeto com esse nome.", "vermelho", True
                        )
                    )
                    sleep(2)
                    system("cls")


        elif opcao == "Renomear Projeto":
            while True:
                print(
                    marcar_textos("Digite 'sair' para voltar pro menu.", "preto", None)
                )
                nome = str(
                    questionary.text("Nome do projeto que vai ser editado: ", qmark="", style=estilo).ask()
                )
                if nome == "sair":
                    break

                elif validar_nome_tabela(nome) == False:
                    while True:
                        novo_nome = str(
                        questionary.text("Novo nome do projeto: ", qmark="", style=estilo).ask()
                    )
                        if novo_nome == "sair":
                            break
                        elif validar_nome_tabela(novo_nome) == True:
                            Projeto(nome).renomear_projeto(novo_nome)
                            linha_menu(tamanho=65, cor="azul", negrito=True)
                            print(marcar_textos("Processando...", "amarelo", True))
                            sleep(2)
                            print(marcar_textos(f'O projeto "{nome}" foi renomeado para "{novo_nome}.', "verde", True))
                            sleep(2)
                            break
                        else:
                            print("Já existe uma tabela com esse nome. ")
                else:
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(
                        marcar_textos(
                            "Não existe nenhuma tabela com esse nome.", "vermelho", True
                        )
                    )
                    sleep(2)
                    system("cls")
                    

        elif opcao == "Ver todos":
            pass

        elif opcao == "Sair":
            break

projeto()