import sqlite3
import sys
sys.path.append('/Users/vinicius/Documents/GitHub/Projeto_agenda')
from datetime import datetime, date, timedelta
from formatacao_e_menu import converter_string_horario_em_timedelta
conexao = sqlite3.connect("estudos.db")
with sqlite3.connect("estudos.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudos (id INTEGER PRIMARY KEY AUTOINCREMENT, registro TEXT NOT NULL, horario_inicial TEXT NOT NULL, horario_final TEXT NOT NULL, data TEXT NOT NULL, avaliacao TEXT NOT NULL)
    """)

class Estudo:
    def __init__(self, anotacao="Sem comentários", horario_inicial="00:00", horario_final="00:00", pausa="00:00", data=date.today()):
        self._anotacao = anotacao
        self._horario_inicial = horario_inicial
        self._horario_final = horario_final
        self._data = str(data)
        self._pausa = pausa
    
    def avaliar_estudos(self):
        horas_de_estudo = datetime.strptime(self._horario_final, "%H:%M") - datetime.strptime(self._horario_inicial, "%H:%M") - converter_string_horario_em_timedelta(self._pausa)
        if horas_de_estudo < timedelta(hours=2):
            return "Seu tempo de estudo foi horrível."
        elif horas_de_estudo > timedelta(hours=2) and horas_de_estudo < timedelta(hours=3):
            return "Seu tempo de estudo foi bom."
        else:
            return "Seu tempo de estudo foi Excelente."


    def registrar_estudo(self):
        avaliacao = self.avaliar_estudos()
        with sqlite3.connect("estudos.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(f"INSERT INTO estudos (registro, horario_inicial, horario_final, data, avaliacao) VALUES (?, ?, ?, ?, ?)", (self._anotacao, self._horario_inicial, self._horario_final, self._data, avaliacao))
            conexao.commit()
