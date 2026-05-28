from datetime import date
from os import system
from time import sleep
from formatacao.funcoes_formatacao import (
    marcar_textos,
    menu_de_opcoes,
    menu_texto,
    linha_menu,
    visualizar_toda_agenda,
)
from validade_autenticacao.validacao import validar
from banco_de_dados.criacao import Atividade, Registro

try:
    while True:
        while True:
            system("cls")
            menu_de_opcoes(
                "MENU",
                "=",
                50,
                "azul",
                "verde",
                True,
                True,
                ["Agenda", "Meus projetos", "Bloco de notas"],
            )
            opcao = input("Opção: ")
            if validar("1234", opcao) == True:
                break
            print("Escolha uma das opções.")
            sleep(2)

        system("cls")

        if opcao == "1":
            try:
                while True:
                    menu_de_opcoes(
                        "AGENDA",
                        "=",
                        50,
                        "amarelo",
                        "ciano",
                        True,
                        True,
                        ["Ver agenda", "Escrever", "Apagar", "Sair"],
                    )
                    opcao_1 = input("opção: ")
                    if validar("1234", opcao_1) == True:
                        break
                    system("cls")

            except Exception as erro:
                print(f"Erro: {erro}")
            system("cls")

            if opcao_1 == "1":
                try:
                    todos_os_registros = Registro().ver_todos()
                    visualizar_toda_agenda(todos_os_registros)
                    sleep(60)
                except Exception as erro:
                    print(f"Erro: {erro}")

            elif opcao_1 == "2":
                try:
                    data_hoje = str(date.today())
                    menu_texto(data_hoje, "=", 50, "branco", "branco", True, True)
                    texto_escrito = input("Escreva: ")
                    Registro(texto_escrito).registrar()
                    print("Processando...")
                    sleep(2)
                    print(marcar_textos("Registro adicionado com sucesso."))
                    sleep(2)
                except Exception as erro:
                    print(f"ERRO: {erro}")

            elif opcao_1 == "3":
                try:
                    menu_de_opcoes("Deletar registro")
                    deletar_id = int(
                        input("Qual o ID do registro que você deseja deletar? ")
                    )
                    lista_de_registros = Registro().ver_todos()
                    for item in lista_de_registros:
                        if item["id"] == deletar_id:
                            Registro().deletar(deletar_id)
                            print("Processando...")
                            sleep(2)
                            print(
                                marcar_textos(
                                    "Registro deletado com sucesso.", "verde", True
                                )
                            )
                            sleep(2)
                            break
                    else:
                        print("Nenhum registro com esse ID foi encontrado.")
                except Exception as erro:
                    print(f"Erro: {erro}")

        elif opcao == "2":
            menu_de_opcoes(
                "Meus projetos",
                "=",
                50,
                "Azul",
                "verde",
                True,
                True,
                [
                    "Ver projetos",
                    "Criar projeto",
                    "Apagar projeto",
                    "Abrir projeto",
                    "Sair",
                ],
            )

        elif opcao == "3":
            menu_de_opcoes(
                "Bloco de notas",
                "=",
                50,
                "Vermelho",
                "amarelo",
                True,
                True,
                ["Ver notas", "Criar nota", "Apagar nota", "Sair"],
            )

except Exception as erro:
    print(f"Erro: {erro}")
