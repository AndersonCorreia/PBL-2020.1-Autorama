
# coding=utf-8
import json
import os
from client.src.mqtt.PUB import Publisher

class Carro:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        dados['carro_id'] = int(dados['carro_id'])
        dados['carro_id'] = self.dados['carros'][-1]['carro_id'] + 1 if len(self.dados['carros']) > 0 else 1
        self.dados["carros"].append(dados)
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False))
        
    def getTags(self):
        connection = self.getConnection()
        connection.request('/config/carro')
        return connection.requestRecv()['headers']

    def getConnection(self):
        return Publisher("node02.myqtthub.com", 1883, "2", "cliente2", "135790")