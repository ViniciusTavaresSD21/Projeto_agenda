import sqlite3
from datetime import datetime
import questionary
from formatacao_e_menu import menu_texto,linha_menu


conexao = sqlite3.connect('registros_diarios.db')
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
""")

class Registro:
    #"""Esse classe representa um registro de um texto"""
    def __init__(self, texto=''):
        self._texto = texto
        self._data_hora = datetime.now().strftime("%d/%m/%Y ás %H:%M")
    
    def registrar(self):
        cursor.execute("INSERT INTO Diario (registro, data) VALUES (?, ?)", (self._texto, self._data_hora))
        conexao.commit()
        conexao.close()
    
    def deletar(self, id):
        cursor.execute("""DELETE FROM Diario WHERE id = ?""", (id,))
        conexao.commit()
        conexao.close()
    
    def ler_registro(self, id):
        linha = cursor.execute(f"SELECT * FROM Diario WHERE id = {id}").fetchone()
        conexao.close()
        return linha
        
    def editar(self, id):
        cursor.execute("UPDATE Diario SET registro = ? WHERE id = ?;", (self._texto, id) )
        conexao.commit()
        conexao.close()

    def ver_todos(self):
        cursor.execute("SELECT * FROM Diario")
        todos_os_registros = cursor.fetchall()
        return todos_os_registros
    
estilo = questionary.Style([
    ('question', 'fg:red'),
    ('highlighted', 'fg:yellow bold'),
    ('instruction', 'fg:gray'),
    ('pointer', 'fg:red'),
    ('', 'fg:green')
    ])

menu_texto("AGENDA", tamanho=50, cor="azul", cor_texto="verde", negrito=True, negrito_texto=True)
opcao = questionary.select("", choices=["Adicionar registro", "Deletar", "editar", "Ver todos"], qmark="", instruction="Use as setas do teclado.", style=estilo).ask()
if opcao == "Adicionar registro":
    linha_menu(tamanho=50, cor="azul", negrito=True)
    print("Fale um pouco sobre o seu dia...")
    print()
    texto = input()