
# coding=utf-8
import json
import os
from client.src.socket_.Client import Client

class Carro:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/carro.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados.append(dados)
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        dados = connection.request('/config/carro', 'POST', 'READ')
    
    def getConnection(self):
        file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"
        leitor = json.loads(open(file, 'r').read() )
        return Client(leitor['ip'], int(leitor['port']), 2048)