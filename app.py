import questionary
from datetime import date
from os import system
from time import sleep
from validacao_e_formatacao.formatacao_e_menu import (
    marcar_textos,
    menu_de_opcoes,
    menu_texto,
    linha_menu,
    visualizar_toda_agenda,
)
from funcoes.agenda import menu_agenda

menu_texto("Organizador")
opcao_do_menu = questionary.select("Use as setas", ["Agenda", "Registro Diarios", "Projeto", "Encerrar"], qmark='', instruction=' ').ask()
if opcao_do_menu == "Agenda":
    menu_agenda()

