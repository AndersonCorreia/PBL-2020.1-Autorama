
# coding=utf-8
import json
import os
from client.src.socket_.Client import Client

class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = dados
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        return connection.request('/config/leitor', "POST", self.dados)

    def testConnection(self):
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        return connection.request('/test', "GET")
    
    def getConnection(self):
        return Client(self.dados['ip'], int(self.dados['port']), 2048)

    def getButton(self):
        return self.getConnection().request('/button', "GET")