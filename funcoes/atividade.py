import sys
import sqlite3
import questionary
sys.path.append('/Users/vinicius/Documents/GitHub/Projeto_agenda')

from funcoes.projeto import Projeto
from time import sleep
from os import system
from validacao import validar_formato_data, validar_titulo_atividade, validar_tempo_da_data
from formatacao_e_menu import linha_menu, menu_texto, marcar_textos
from textwrap import fill

conexao = sqlite3.connect("projetos.db")

estilo = questionary.Style(
    [
        ("question", "fg:red"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:red"),
        ("", "fg:green"),
    ]
)


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

    def deletar(self, titulo):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"""DELETE FROM {self._nome_da_pasta} WHERE titulo = ?""", (titulo,)
            )
        conexao.commit()

    def editar_titulo(self, titulo, novo_titulo):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE {self._nome_da_pasta} SET titulo = ? WHERE titulo = ?;",
                (novo_titulo, titulo),
            )
        conexao.commit()

    def editar_descricao(self, titulo, nova_descricao):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE {self._nome_da_pasta} SET descricao = ? WHERE titulo = ?;",
                (nova_descricao, titulo),
            )
        conexao.commit()

    def editar_prazo(self, nome_da_atividade, novo_prazo):
        with sqlite3.connect("projetos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE {self._nome_da_pasta} SET prazo = ? WHERE titulo = ?;",
                (novo_prazo, nome_da_atividade),
            )
        conexao.commit()

    def visualizar(self):
        try:
            with sqlite3.connect("projetos.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(f"""SELECT titulo from {self._nome_da_pasta}""")
                lista_titulos = [linha[0] for linha in cursor.fetchall()]
                return lista_titulos
        except Exception as erro:
            print(f"ERRO: {erro}")

    def exibir(self):
        try:
            with sqlite3.connect("projetos.db") as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()
                cursor.execute(f"SELECT * FROM {self._nome_da_pasta}")
                atividades = cursor.fetchall()

            if len(atividades) != 0:
                for atividade in atividades:
                    if atividade["status"] == "Não concluído":
                        cor = "ciano"
                    elif atividade["status"] == "Conluído":
                        cor = "verde"
                    elif atividade["status"] == "Atraso":
                        cor == "vermelho"
                    elif atividade["status"] == "Cancelado":
                        cor == "cinza"

                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(
                        f"{marcar_textos("Titulo:", "amarelo", True)} {marcar_textos(atividade["titulo"], "ciano")}"
                    )
                    print(
                        f"{marcar_textos("Prazo:", "amarelo", True)} {marcar_textos(atividade["prazo"], "ciano")}"
                    )
                    print(
                        f"{marcar_textos("Status:", "amarelo", True)} {marcar_textos(atividade["status"], cor)}"
                    )
                    print()
                    print(f"{marcar_textos("Descrição: ", "amarelo", True)}")
                    print(f"{marcar_textos(fill(atividade["descricao"], 50), "verde")}")
                    linha_menu(tamanho=60, cor="azul", negrito=True)

            else:
                print("Esse projeto não tem nenhuma atividade.")
        except Exception as erro:
            print(f"ERRO: {erro}")


def menu_atividade(pasta_do_projeto):
    while True:
        system("cls")
        menu_texto(
            "ATIVIDADES",
            tamanho=60,
            cor="azul",
            cor_texto="verde",
            negrito=True,
            negrito_texto=True,
        )
        opcao = questionary.select(
            "",
            choices=[
                "Criar atividade",
                "Deletar atividade",
                "Renomear atividade",
                "Editar descrição",
                "Editar prazo",
                "Todas as atividades",
                "Sair",
            ],
            qmark="",
            instruction="Use as setas do teclado",
            style=estilo,
        ).ask()
        linha_menu(tamanho=60, cor="azul", negrito=True)

        if opcao == "Criar atividade":
            while True:
                while True:
                    print(
                        marcar_textos(
                            "Digite 'sair' para voltar pro menu.", "preto", None
                        )
                    )
                    titulo_da_atividade = str(
                        questionary.text(
                            "Titulo da atividade: ", qmark="", style=estilo
                        ).ask()
                    )
                    if (
                        validar_titulo_atividade(pasta_do_projeto, titulo_da_atividade)
                        == True
                    ):
                        print("Já existe uma atividade com esse nome.")
                        sleep(2)
                        system("cls")
                        linha_menu(tamanho=60, cor="azul", negrito=True)
                    else:
                        break

                if titulo_da_atividade.lower() == "sair":
                    break

                else:
                    descricao = questionary.text(
                        "Descrição: ", qmark="", style=estilo
                    ).ask()
                    while True:
                        prazo = questionary.text(
                            "Prazo final (dia/mês/ano): ", qmark="", style=estilo
                        ).ask()
                        if validar_formato_data(prazo) == True:
                            if validar_tempo_da_data(prazo, "posterior") == True:
                                break
                            else:
                                print("O prazo não pode ser anterior a data de hoje.")
                                sleep(2)
                                system("cls")
                        else:
                            print("Digite a data no formato dia/mês/ano.")
                            sleep(2)
                            system("cls")

                    Atividade(
                        pasta_do_projeto, titulo_da_atividade, descricao, prazo
                    ).criar()
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(marcar_textos("Atividade criada.", "verde", True))
                    sleep(2)
                    break

        elif opcao == "Deletar atividade":
            while True:
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
                )
                lista_atividades = Atividade(pasta_do_projeto).visualizar()
                lista_atividades.append("Sair")
                nome = questionary.select(
                    "Selecione a atividade: ",
                    lista_atividades,
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()
                if nome.lower() == "sair":
                    break

                else:
                    Atividade(pasta_do_projeto).deletar(nome)
                    linha_menu(tamanho=60, cor="azul", negrito=True)
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos(
                            f"A atividade '{nome}' foi deletada.", "verde", True
                        )
                    )
                    sleep(2)
                    break

        elif opcao == "Renomear atividade":
            while True:
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
                )

                lista_atividades = Atividade(pasta_do_projeto).visualizar()
                lista_atividades.append("Sair")
                nome = questionary.select(
                    "Selecione o atividade que vai ser renomeado:",
                    lista_atividades,
                    instruction=" ",
                    style=estilo,
                    qmark="",
                ).ask()

                if nome.lower() == "sair":
                    break

                else:
                    novo_nome = str(
                        questionary.text(
                            "Novo nome da atividade: ", qmark="", style=estilo
                        ).ask()
                    )
                    if novo_nome.lower() == "sair":
                        break

                    else:
                        Atividade(pasta_do_projeto).editar_titulo(nome, novo_nome)
                        linha_menu(tamanho=60, cor="azul", negrito=True)
                        print(marcar_textos("Processando...", "amarelo", True))
                        sleep(2)
                        print(
                            marcar_textos(
                                f'A atividade "{nome}" foi renomeada para "{novo_nome}.',
                                "verde",
                                True,
                            )
                        )
                        sleep(2)
                        break

        elif opcao == "Editar descrição":
            while True:
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
                )
                lista_atividades = Atividade(pasta_do_projeto).visualizar()
                lista_atividades.append("Sair")

                nome = questionary.select(
                    "Selecione a atividade que vai ser editada:",
                    lista_atividades,
                    instruction=" ",
                    style=estilo,
                    qmark="",
                ).ask()

                if nome.lower() == "sair":
                    break
                else:
                    nova_descricao = str(
                        questionary.text(
                            "Nova descrição: ", qmark="", style=estilo
                        ).ask()
                    )
                    if nova_descricao.lower() == "sair":
                        break

                    else:
                        Atividade(pasta_do_projeto).editar_descricao(
                            nome, nova_descricao
                        )
                        linha_menu(tamanho=65, cor="azul", negrito=True)
                        print(marcar_textos("Processando...", "amarelo", True))
                        sleep(2)
                        print(
                            marcar_textos(
                                f'A descrição da atividade "nome", foi alterada.',
                                "verde",
                                True,
                            )
                        )
                        sleep(2)
                        break

        elif opcao == "Editar prazo":
            while True:
                print(
                    marcar_textos(
                        "Selecione 'Sair' para voltar pro menu.", "preto", None
                    )
                )
                lista_atividades = Atividade(pasta_do_projeto).visualizar()
                lista_atividades.append("Sair")

                nome = questionary.select(
                    "Selecione a atividade que vai ser editada:",
                    lista_atividades,
                    instruction=" ",
                    style=estilo,
                    qmark="",
                ).ask()
                if nome.lower() == "sair":
                    break

                else:
                    while True:
                        linha_menu(tamanho=60, cor="azul", negrito=True)
                        print(
                            marcar_textos(
                                'Se a atividade não tiver um pravo final, digite "sem prazo"',
                                "preto",
                                None,
                            )
                        )
                        novo_prazo = questionary.text(
                            "Novo prazo final (dia/mês/ano): ", qmark="", style=estilo
                        ).ask()
                        if novo_prazo.lower() == "sair":
                            break

                        elif (
                            validar_formato_data(novo_prazo) == True
                            or novo_prazo == "sem prazo"
                        ):
                            if validar_tempo_da_data(novo_prazo, "posterior"):
                                try:
                                    if novo_prazo == "sem prazo":
                                        novo_prazo = None
                                    Atividade(pasta_do_projeto).editar_prazo(
                                        novo_prazo, nome
                                    )
                                    linha_menu(tamanho=60, cor="azul", negrito=True)
                                    print(
                                        marcar_textos("Processando...", "amarelo", True)
                                    )
                                    sleep(2)
                                    print(
                                        marcar_textos(
                                            f'O prazo final da atividade "nome", foi alterado.',
                                            "verde",
                                            True,
                                        )
                                    )
                                    sleep(2)
                                    break
                                except Exception as erro:
                                    print(
                                        f"{marcar_textos("ERRO", "vermelho", True)} o"
                                    )
                                    sleep(3)
                                    break
                            else:
                                print("O prazo não pode ser anterior a data de hoje.")
                                sleep(2)
                                system("cls")
                        else:
                            print("Digite a data no formato dia/mês/ano.")
                            sleep(2)
                            system("cls")
                break

        elif opcao == "Todas as atividades":
            while True:
                Atividade(pasta_do_projeto).exibir()
                print(marcar_textos("Aperte enter para sair.", "preto"))
                input()
                break

        elif opcao == "Sair":
            break


menu_atividade("teste")
