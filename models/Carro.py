
# coding=utf-8
import json
import os
from client.src.socket_.Client import Client

class Carro:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        dados['carro_id'] = int(dados['carro_id'])
        dados['carro_id'] = self.dados['carros'][-1]['carro_id'] + 1 if len(self.dados['carros']) > 0 else 1
        self.dados["carros"].append(dados)
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False))
        
    def getTag(self):
        connection = self.getConnection()
        try:
            return connection.request('/configuração/carro', 'GET', '')['response']
        except RuntimeError as error:
            return 0
    
    def getConnection(self):
        file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"
        leitor = json.loads(open(file, 'r').read() )
        return Client(leitor['ip'], int(leitor['port']), 2048)