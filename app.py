from funcoes import agenda, estudos, projeto
from formatacao_e_menu import marcar_textos, menu_texto, linha_menu
from questionary import select, Style
from time import sleep
from os import system


estilo = Style(
    [
        ("question", "fg:cyan bold"),
        ("highlighted", "fg:yellow bold"),
        ("instruction", "fg:gray"),
        ("pointer", "fg:cyan"),
        ("", "fg:green"),
    ]
)

while True:
    system("cls")
    menu_texto("MENU", cor="azul", cor_texto="verde", negrito=True, negrito_texto=True)
    opcao = select("", ["Agenda", "Estudos", "Projetos", "Encerrar"], qmark="", instruction="Use as setas do teclado.", style=estilo).ask()
    if opcao == "Agenda":
        agenda.menu_agenda()
    elif opcao == "Estudos":
        estudos.menu_estudos()
    elif opcao == "Projetos":
        projeto.menu_projeto()
    else:
        linha_menu(tamanho=60, cor="azul", negrito=True)
        print(marcar_textos("Encerrando...","amarelo", True))
        sleep(2)
        print(marcar_textos("Programa encerrado.", "amarelo", True))
        break

