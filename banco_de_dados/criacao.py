import sqlite3
from datetime import datetime

conexao = sqlite3.connect('registros_diarios.db')
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS atividades (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL, prazo TEXT NOT NULL, status TEXT NOT NULL)
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
    

class Atividade:
    def __init__(self, titulo="Sem titulo", descricao="", prazo=None):
        self._titulo = titulo
        self._descricao = descricao
        self._prazo = prazo
        self._status = "Não concluído"
    
    def criar(self, prazo):
        cursor.execute(f"INSERT INTO atividades (titulo, descricao, prazo, status) VALUES (?, ?, ?, ?)", (self._titulo, self._descricao, prazo, self._status))
        conexao.commit()
        conexao.close()
    
    def deletar(self, id):
        cursor.execute("""DELETE FROM atividades WHERE id = ?""", (id,))
        conexao.commit()
        conexao.close()
    
    def ler_atividade(self, id):
        linha = cursor.execute(f"SELECT * FROM atividades WHERE id = {id}").fetchone()
        conexao.close()
        return linha
    
    def editar_titulo(self, id):
        cursor.execute("UPDATE atividades SET titulo = ? WHERE id = ?;", (self._titulo, id) )
        conexao.commit()
        conexao.close()
    
    def editar_descricao(self, id):
        cursor.execute("UPDATE atividades SET descricao = ? WHERE id = ?;", (self._descricao, id) )
        conexao.commit()
        conexao.close()
       
    def editar_prazo(self, id):
        cursor.execute("UPDATE atividade SET prazo = ? WHERE id = ?;", (self._prazo, id))
        cursor.commit()
        conexao.close()

