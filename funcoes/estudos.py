import sqlite3
import sys
import questionary
from os import system
from time import sleep
from textwrap import fill

sys.path.append("/Users/vinicius/Documents/GitHub/Projeto_agenda")

from datetime import datetime, date, timedelta
from formatacao_e_menu import (
    converter_string_horario_em_timedelta,
    menu_texto,
    linha_menu,
    marcar_textos,
)
from validacao import avaliar_estudos

conexao = sqlite3.connect("estudos.db")
with sqlite3.connect("estudos.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudos (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, horario_inicial TEXT NOT NULL, horario_final TEXT NOT NULL, data TEXT NOT NULL, tempo_de_estudo, avaliacao TEXT NOT NULL)
    """)

estilo = questionary.Style(
    [
        ("question", "fg:cyan bold"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:cyan"),
        ("", "fg:green"),
    ]
)


class Estudo:
    def __init__(
        self,
        anotacao="Sem comentários",
        horario_inicial="00:00",
        horario_final="00:00",
        pausa="00:00",
        data=date.today(),
    ):
        self._anotacao = anotacao
        self._horario_inicial = horario_inicial
        self._horario_final = horario_final
        self._data = str(datetime.strftime(data, "%d/%m/%Y"))
        self._pausa = pausa
        self._horas_de_estudo = (
            datetime.strptime(self._horario_final, "%H:%M")
            - datetime.strptime(self._horario_inicial, "%H:%M")
            - converter_string_horario_em_timedelta(self._pausa)
        )

    def registrar_estudo(self):
        avaliacao = avaliar_estudos(self._horas_de_estudo)
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"INSERT INTO estudos (registro, horario_inicial, horario_final, data, tempo_de_estudo, avaliacao) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    self._anotacao,
                    self._horario_inicial,
                    self._horario_final,
                    self._data,
                    str(self._horas_de_estudo),
                    avaliacao,
                ),
            )
            conexao.commit()

    def editar_tempo_estudo(self, horario_inicial, horario_final, data, pausa="00:00"):
        horas_de_estudo = (
            datetime.strptime(horario_final, "%H:%M")
            - datetime.strptime(horario_inicial, "%H:%M")
            - converter_string_horario_em_timedelta(pausa)
        )
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE estudos SET (tempo_de_estudo, horario_final, horario_inicial, avaliacao) = (?, ?, ?, ?) WHERE data = ?",
                (
                    str(horas_de_estudo),
                    horario_final,
                    horario_inicial,
                    avaliar_estudos(horas_de_estudo),
                    data,
                ),
            )
            conexao.commit()

    def editar_data(self, data_anterior, nova_data):
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE estudos SET data = ? WHERE data = ?",
                (nova_data, data_anterior),
            )
            conexao.commit()

    def editar_comentario(self, comentario_antigo, novo_comentario):
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                f"UPDATE estudos SET registro = ? WHERE registro = ?",
                (novo_comentario, comentario_antigo),
            )
            conexao.commit()

    def deletar_registro(self, data):
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(f"DELETE FROM estudos WHERE data = ?", (data))
            conexao.commit()

    def visualizar_registro(self, registro):
        linha_menu(tamanho=60, cor="azul", negrito=True)
        print(
            f"{marcar_textos("ID:", "amarelo", True)} {marcar_textos(registro["id"], "ciano")}"
        )
        print(
            f"{marcar_textos("Data:", "amarelo", True)} {marcar_textos(registro["data"], "ciano")}"
        )
        print(
            f"{marcar_textos("Prazo:", "amarelo", True)} {marcar_textos(registro["tempo_de_estudo"], "ciano")}"
        )
        print(
            f"{marcar_textos("Status:", "amarelo", True)} {marcar_textos(registro["avaliacao"], "ciano")}"
        )
        print()
        print(f"{marcar_textos("Comentário: ", "amarelo", True)}")
        print(f"{marcar_textos(fill(registro["registro"], 50), "verde")}")
        linha_menu(tamanho=60, cor="azul", negrito=True)


def menu_estudos():
    while True:
        system("cls")
        menu_texto(
            "ESTUDOS DIARIOS",
            tamanho=60,
            cor="azul",
            cor_texto="verde",
            negrito=True,
            negrito_texto=True,
        )
        opcao = questionary.select(
            "",
            choices=["Registrar estudo", "Deletar registro", "Ver registros", "Sair"],
            qmark="",
            instruction="Use as setas do teclado",
            style=estilo,
        ).ask()
        linha_menu(tamanho=60, cor="azul", negrito=True)

        if opcao == "Registrar estudo":
            system("cls")
            menu_texto(
                "REGISTRANDO ESTUDOS:",
                cor="azul",
                cor_texto="verde",
                negrito=True,
                negrito_texto=True,
            )
            while True:
                print(
                    marcar_textos("Digite 'sair' para voltar pro menu.", "preto", None)
                )
                comentario = str(
                    questionary.text(
                        "Faça uma anotação: ", qmark="", style=estilo
                    ).ask()
                )

                if comentario.lower() == "sair":
                    break

                elif len(comentario) == 0:
                    comentario = "Sem comentários."

                while True:
                    horario_de_inicio = questionary.text(
                        "Horario de inicio (hora:minuto): ", qmark="", style=estilo
                    ).ask()

                    if horario_de_inicio.lower() == "sair":
                        return

                    try:
                        datetime.strptime(horario_de_inicio, "%H:%M")
                        break
                    except:
                        linha_menu(cor="azul", negrito=True)
                        print(
                            marcar_textos(
                                'Formato inválido. Digite o horario no formato "hora:minuto".',
                                "amarelo",
                                True,
                            )
                        )
                        sleep(2)
                        system("cls")
                        linha_menu(cor="azul", negrito=True)

                while True:
                    horario_de_termino = questionary.text(
                        "Horario de fim (hora:minuto): ", qmark="", style=estilo
                    ).ask()

                    if horario_de_termino.lower() == "sair":
                        return

                    try:
                        datetime.strptime(horario_de_termino, "%H:%M")
                        break
                    except:
                        linha_menu(cor="azul", negrito=True)
                        print(
                            marcar_textos(
                                'Formato inválido. Digite o horario no formato "hora:minuto".',
                                "amarelo",
                                True,
                            )
                        )
                        sleep(2)
                        system("cls")
                        linha_menu(cor="azul", negrito=True)

                opcao = questionary.select(
                    "Você fez alguma pausa? ",
                    choices=["Sim", "Não"],
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()
                if opcao == "Sim":
                    while True:
                        pausa = questionary.text(
                            "Tempo de pausa(hora:minuto): ", qmark="", style=estilo
                        ).ask()

                        if pausa.lower() == "sair":
                            return

                        try:
                            datetime.strptime(horario_de_inicio, "%H:%M")
                            break

                        except:
                            linha_menu(cor="azul", negrito=True)
                            print(
                                marcar_textos(
                                    'Formato inválido. Digite o horario no formato "hora:minuto".',
                                    "amarelo",
                                    True,
                                )
                            )
                            sleep(2)
                            system("cls")
                            linha_menu(cor="azul", negrito=True)

                else:
                    pausa = "00:00"
                linha_menu(cor="azul", negrito=True)
                Estudo(
                    comentario, horario_de_inicio, horario_de_termino, pausa
                ).registrar_estudo()
                print(marcar_textos("Processando...", "amarelo", True))
                sleep(2)
                print(marcar_textos("Registro feito com sucesso.", "verde", True))
                sleep(2)
                break

        elif opcao == "Deletar registro":
            system("cls")
            menu_texto(
                "DELETANDO ESTUDOS",
                cor="azul",
                cor_texto="verde",
                negrito=True,
                negrito_texto=True,
            )
            while True:
                with sqlite3.connect("estudos.db") as conexao:
                    cursor = conexao.cursor()
                    cursor.execute(f"""SELECT data from estudos""")
                    lista = [linha[0] for linha in cursor.fetchall()]
                    lista_de_datas = ["Sair"]
                    for item in lista:
                        if item not in lista_de_datas:
                            lista_de_datas.insert(0, item)

                data = questionary.select(
                    "Qual a data do registro que você deseja deletar? ",
                    lista_de_datas,
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()
                if data == "Sair":
                    break

                if lista.count(data) > 1:
                    with sqlite3.connect("estudos.db") as conexao:
                        conexao.row_factory = sqlite3.Row
                        cursor = conexao.cursor()
                        lista_da_data = cursor.execute(
                            f"SELECT * FROM estudos WHERE data = ?", (data,)
                        )

                    lista_de_registro = ["Sair"]
                    for item in lista_da_data:
                        lista_de_registro.insert(0, item["registro"])

                    linha_menu(cor="azul", negrito=True)
                    registro_a_ser_deletado = questionary.select(
                        "Qual registro você quer deletar?",
                        lista_de_registro,
                        qmark="",
                        instruction=" ",
                        style=estilo,
                    ).ask()

                    if registro_a_ser_deletado == "Sair":
                        break

                    linha_menu(cor="azul", negrito=True)
                    cursor.execute(
                        "DELETE FROM estudos WHERE registro = ?",
                        (str(registro_a_ser_deletado),),
                    )
                    conexao.commit()
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos("Registro deletado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    break

                else:
                    linha_menu(cor="azul", negrito=True)
                    cursor.execute("DELETE FROM estudos WHERE data = ?", (data,))
                    conexao.commit()
                    print(marcar_textos("Processando...", "amarelo", True))
                    sleep(2)
                    print(
                        marcar_textos("Registro deletado com sucesso.", "verde", True)
                    )
                    sleep(2)
                    break

        elif opcao == "Ver registros":

            while True:
                system("cls")
                menu_texto(
                    "VISUALIZANDO:",
                    cor="azul",
                    cor_texto="verde",
                    negrito=True,
                    negrito_texto=True,
                )
                with sqlite3.connect("estudos.db") as conexao:
                    cursor = conexao.cursor()
                    cursor.execute(f"""SELECT data from estudos""")
                    lista = [linha[0] for linha in cursor.fetchall()]
                    lista_de_datas = ["Sair"]
                    for item in lista:
                        if item not in lista_de_datas:
                            lista_de_datas.insert(0, item)

                data = questionary.select(
                    "Qual a data do registro que você deseja ver? ",
                    lista_de_datas,
                    qmark="",
                    instruction=" ",
                    style=estilo,
                ).ask()
                if data == "Sair":
                    break

                if lista.count(data) > 1:
                    with sqlite3.connect("estudos.db") as conexao:
                        conexao.row_factory = sqlite3.Row
                        cursor = conexao.cursor()
                        lista_da_data = cursor.execute(
                            f"SELECT * FROM estudos WHERE data = ?", (data,)
                        )

                    lista_de_registro = ["Sair"]
                    for item in lista_da_data:
                        lista_de_registro.insert(0, item["registro"])

                    linha_menu(cor="azul", negrito=True)
                    registro_selecionado = questionary.select(
                        "Qual registro você quer visualizar?",
                        lista_de_registro,
                        qmark="",
                        instruction=" ",
                        style=estilo,
                    ).ask()

                    if registro_selecionado == "Sair":
                        break

                    registro = list(
                        cursor.execute(
                            f"SELECT * FROM estudos WHERE registro = ?",
                            (registro_selecionado,),
                        )
                    )
                    registro = dict(registro[0])
                    Estudo().visualizar_registro(registro)
                    opcao = questionary.select(
                        "Você deseja editar esse registro?",
                        ["Sim", "Não"],
                        qmark="",
                        instruction=" ",
                        style=estilo,
                    ).ask()
                    linha_menu(cor="azul", negrito=True)
                    if opcao == "Sim":
                        opcao2 = questionary.select(
                            "Qual informação você deseja editar?",
                            ["Data", "Tempo de estudos", "Comentário", "Sair"],
                            qmark="",
                            instruction=" ",
                            style=estilo,
                        ).ask()
                        if opcao2 == "Data":
                            while True:
                                system("cls")
                                menu_texto("Editando data")
                                try:
                                    nova_data = comentario = str(
                                        questionary.text(
                                            "Nova data (dia/Mês/ano):",
                                            qmark="",
                                            style=estilo,
                                        ).ask()
                                    )
                                    if nova_data.lower() == "sair":
                                        system("cls")
                                        break
                                    datetime.strptime(nova_data, "%d/%m/%Y")
                                    Estudo().editar_data(registro["data"], nova_data)
                                    print(
                                        marcar_textos("Processando...", "amarelo", True)
                                    )
                                    sleep(2)
                                    print(
                                        marcar_textos(
                                            "Data editada com sucesso.", "verde", True
                                        )
                                    )
                                    sleep(2)
                                    break
                                except:
                                    print(
                                        "Formato inválido. Digite a data no formato dia/mês/ano"
                                    )

                        elif opcao2 == "Tempo de estudos":
                            while True:
                                system("cls")
                                menu_texto("Editando tempo")
                                try:
                                    inicio = str(
                                        questionary.text(
                                            "Horario de Inicio: ",
                                            qmark="",
                                            style=estilo,
                                        ).ask()
                                    )
                                    if inicio.lower() == "sair":
                                        system("cls")
                                        break

                                    fim = str(
                                        questionary.text(
                                            "Horario de Termino: ",
                                            qmark="",
                                            style=estilo,
                                        ).ask()
                                    )
                                    if fim.lower() == "sair":
                                        system("cls")
                                        break

                                    pausa = questionary.select(
                                        "Você fez alguma pausa?",
                                        ["Sim", "Não"],
                                        qmark="",
                                        style=estilo,
                                    ).ask()
                                    if pausa == "Não":
                                        pausa = "00:00"
                                    elif pausa == "Sim":
                                        pausa = questionary.text(
                                            "Tempo de pausa:",
                                            qmark="",
                                            instruction=" ",
                                            style=estilo,
                                        ).ask()

                                    datetime.strptime(inicio, "%H:%M")
                                    datetime.strptime(fim, "%H:%M")
                                    datetime.strptime(pausa, "%H:%M")
                                    Estudo().editar_tempo_estudo(
                                        inicio, fim, registro["data"], pausa
                                    )
                                    print(
                                        marcar_textos("Processando...", "amarelo", True)
                                    )
                                    sleep(2)
                                    print(
                                        marcar_textos(
                                            "Tempo de estudo editado com sucesso.",
                                            "verde",
                                            True,
                                        )
                                    )
                                    sleep(2)
                                    break
                                except:
                                    linha_menu(cor="azul", negrito=True)
                                    print(
                                        marcar_textos(
                                            "Formato inválido. Digite a data no formato dia/mês/ano",
                                            "amarelo",
                                            True,
                                        )
                                    )
                                    sleep(2)
                                    system("cls")

                        elif opcao2 == "Comentário":
                            system("cls")
                            menu_texto("EDITANDO COMENTÁRIO")
                            novo_comentario = questionary.text(
                                "Novo comentário: ", qmark="", style=estilo
                            ).ask()
                            if novo_comentario.lower() == "sair":
                                break

                            Estudo().editar_comentario(
                                registro["registro"], novo_comentario
                            )
                            print(marcar_textos("Processando...", "amarelo", True))
                            sleep(2)
                            print(
                                marcar_textos(
                                    "Comentário editada com sucesso.", "verde", True
                                )
                            )
                            sleep(2)
                            break

                        elif opcao2 == "Sair":
                            input(
                                marcar_textos("Aperte enter para sair.", "preto", True)
                            )
                            break

                    elif opcao == "Não":
                        input(marcar_textos("Aperte enter para sair.", "preto", True))
                        break

                else:
                    input(marcar_textos("Aperte enter para sair.", "preto", True))
                    break

        elif opcao == "Sair":
            break