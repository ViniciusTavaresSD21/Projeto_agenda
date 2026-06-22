from projeto import Projeto
import sqlite3
import questionary
from time import sleep
from os import system
from validacao import validar_nome_tabela, validar_titulo_atividade, validar_formato_data
from formatacao_e_menu import menu_texto, linha_menu, marcar_textos

conexao = sqlite3.connect("projetos.db")

class Atividade(Projeto):
    def __init__(self, nome_da_pasta, titulo="Sem titulo", descricao="", prazo=None):
        self._titulo = titulo
        self._descricao = descricao
        self._prazo = prazo
        self._status = "Não concluído"
        super().__init__(nome_da_pasta)


    def criar(self):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"INSERT INTO {self._nome_da_pasta} (titulo, descricao, prazo, status) VALUES (?, ?, ?, ?)",
            (self._titulo, self._descricao, self._prazo, self._status),
        )
        conexao.commit()


    def deletar(self, id):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"""DELETE FROM {self._nome_da_pasta} WHERE id = ?""", (id,)
        )
        conexao.commit()


    def ler_atividade(self, id):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            linha = cursor.execute(
            f"SELECT * FROM {self._nome_da_pasta} WHERE id = {id}"
        ).fetchone()
        conexao.close()
        return linha


    def editar_titulo(self, id):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"UPDATE {self._nome_da_pasta} SET titulo = ? WHERE id = ?;",
            (self._titulo, id),
        )
        conexao.commit()


    def editar_descricao(self, id):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            f"UPDATE {self._nome_da_pasta} SET descricao = ? WHERE id = ?;",
            (self._descricao, id),
        )
        conexao.commit()


    def editar_prazo(self, id):
        with sqlite3.connect("projetos.db") as conexao:
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


def menu_atividade(pasta_do_projeto):
     while True:
        system("cls")
        menu_texto(
            "ATIVIDADES",
            tamanho=65,
            cor="azul",
            cor_texto="verde",
            negrito=True,
            negrito_texto=True,
        )
        opcao = questionary.select(
            "",
            choices=["Criar atividade", "Deletar atividade", "Renomear atividade", "Ver todas atividades", "Sair"],
            qmark="",
            instruction="Use as setas do teclado",
            style=estilo,
        ).ask()
        linha_menu(tamanho=65, cor="azul", negrito=True)

        if opcao == "Criar atividade":
            while True:
                while True:
                    print(
                        marcar_textos("Digite 'sair' para voltar pro menu.", "preto", None)
                    )
                    titulo_da_atividade = str(
                        questionary.text("Titulo da atividade: ", qmark="", style=estilo).ask()
                    )
                    if validar_titulo_atividade(pasta_do_projeto, titulo_da_atividade) == True:
                        print("Já existe uma atividade com esse nome.")
                        sleep(2)
                        system('cls')
                        linha_menu(tamanho=65, cor="azul", negrito=True)
                    else:
                        break

                if titulo_da_atividade == "sair":
                        break

                else:
                    descricao = questionary.text("Descrição: ", qmark="", style=estilo).ask()
                    while True:
                        prazo = questionary.text("Prazo final (dia/mês/ano): ", qmark="", style=estilo).ask()
                        if validar_formato_data(prazo) == True:
                            break
                        else:
                            print("Digite a data no formato dia/mês/ano.")
                            sleep(2)
                            system('cls')

                    Atividade(pasta_do_projeto, titulo_da_atividade, descricao, prazo).criar()
                    linha_menu(tamanho=65, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(marcar_textos("Atividade criada.", "verde", True))
                    sleep(2)
                    break