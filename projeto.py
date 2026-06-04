import sqlite3
from datetime import datetime

conexao = sqlite3.connect('registros_diarios.db')
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Diario (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, data TEXT NOT NULL)
""")

class Projeto():
    def __init__(self, nome_da_pasta):
        self._nome_da_pasta = nome_da_pasta
        

    def criar_projeto(self):
        nome = str(self._nome_da_pasta)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome} (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL, prazo TEXT NOT NULL, status TEXT NOT NULL)")
        
    
class Atividade(Projeto):
    def __init__(self, nome_da_pasta, titulo="Sem titulo", descricao="", prazo=None):
        self._titulo = titulo
        self._descricao = descricao
        self._prazo = prazo
        self._status = "Não concluído"
        self._nome_da_pasta = nome_da_pasta
    

    def criar(self, prazo):
        cursor.execute(f"INSERT INTO {self._nome_da_pasta} (titulo, descricao, prazo, status) VALUES (?, ?, ?, ?)", (self._titulo, self._descricao, prazo, self._status))
        conexao.commit()
        conexao.close()
    

    def deletar(self, id):
        cursor.execute(f"""DELETE FROM {self._nome_da_pasta} WHERE id = ?""", (id,))
        conexao.commit()
        conexao.close()
    

    def ler_atividade(self, id):
        linha = cursor.execute(f"SELECT * FROM {self._nome_da_pasta} WHERE id = {id}").fetchone()
        conexao.close()
        return linha
    

    def editar_titulo(self, id):
        cursor.execute(f"UPDATE {self._nome_da_pasta} SET titulo = ? WHERE id = ?;", (self._titulo, id) )
        conexao.commit()
        conexao.close()
    

    def editar_descricao(self, id):
        cursor.execute(f"UPDATE {self._nome_da_pasta} SET descricao = ? WHERE id = ?;", (self._descricao, id) )
        conexao.commit()
        conexao.close()
       

    def editar_prazo(self, id):
        cursor.execute(f"UPDATE {self._nome_da_pasta} SET prazo = ? WHERE id = ?;", (self._prazo, id))
        cursor.commit()
        conexao.close()