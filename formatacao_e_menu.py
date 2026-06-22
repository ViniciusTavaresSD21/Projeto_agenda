def marcar_textos(texto, cor=None, negrito=None):
    cor = cor.lower() if cor != None else cor

    if cor == "preto":
        cor = 30

    elif cor == "vermelho":
        cor = 31

    elif cor == "verde":
        cor = 32

    elif cor == "amarelo":
        cor = 33

    elif cor == "azul":
        cor = 34

    elif cor == "magenta":
        cor = 35

    elif cor == "ciano":
        cor = 36

    elif cor == "branco":
        cor = 37

    else:
        cor == None

    if cor == None and negrito == True:
        return f"\033[1m{texto}\033[m"

    if negrito == True:
        return f"\033[1;{cor}m{texto}\033[m"
    else:
        return f"\033[{cor}m{texto}\033[m"


def linha_menu(simbolo="=", tamanho=60, cor="branco", negrito=None):
    print(marcar_textos(simbolo * tamanho, cor, negrito))


def menu_texto(
    texto,
    simbolo="=",
    tamanho=60,
    cor="branco",
    cor_texto="branco",
    negrito=None,
    negrito_texto=None,
):
    linha_menu(simbolo, tamanho, cor, negrito)
    print(marcar_textos(f"{texto:^{tamanho}}", cor_texto, negrito_texto))
    linha_menu(simbolo, tamanho, cor, negrito)


def menu_de_opcoes(
    texto,
    simbolo="=",
    tamanho=60,
    cor="branco",
    cor_texto="branco",
    negrito=None,
    negrito_texto=None,
    opcoes=[],
):
    menu_texto(texto, simbolo, tamanho, cor, cor_texto, negrito, negrito_texto)
    contador = 1
    for op in opcoes:
        print(f"\033[1m[{contador}] {op}\033[m")
        contador += 1
    linha_menu(simbolo, tamanho, cor)


def visualizar_toda_agenda(dict):
    menu_texto(
        "Todos os registro", tamanho=50,
        cor="ciano",
        cor_texto="verde",
        negrito=True,
        negrito_texto=True,
    )
    for item in dict:
        print(marcar_textos(f"ID: {item["id"]}", negrito=True))
        print(marcar_textos(f"DATA: {item["data"]}", negrito=True))
        print()
        print(marcar_textos("Registro:", negrito=True))
        print(marcar_textos(item["registro"], "preto", True))
        linha_menu(tamanho=50, cor="verde")
