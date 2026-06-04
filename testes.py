import questionary

first_name = questionary.select("", choices=["Agenda", "Meus projetos", "Bloco de notas"], instruction="Use as setas do teclado").ask()