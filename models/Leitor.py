
# coding=utf-8
import json
import os
from client.socket_ import Client

class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = dados
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        connection.request('/config/leitor', "POST", self.dados)
    
    def getConnection(self):
        return Client(self.dados['ip'], self.dados['port'], 2048)