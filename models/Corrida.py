
# coding=utf-8
from client.src.socket_.Client import Client
from models.Autorama import Autorama
from models.Leitor import Leitor

class Corrida:
    def __init__(self, corrida_id):
        self.autorama = Autorama()
        self.leitor = Leitor()
        self.corrida = self.autoram.getCorrida(corrida_id)
    
    def save(self, dados):
        self.autoram.saveCorrida(self.corrida)
        
    def qualificatoria(self):
        connection = self.leitor.getConnection()
        connection.request('/corrida/qualificatoria/carros', 'POST', self.corrida['pilotos'])#informa ao leitor quais as tags que devem ser lidas
        connection.requestOpen('/corrida/qualificatoria/acompanhar', 'GET', '')
        corridaEnd = False
        while not CorridaEnd:
            result = connection.requestRecv()#aguarda o leitor responder com uma tag
        connection.requestClose