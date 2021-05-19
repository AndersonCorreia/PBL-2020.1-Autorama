# coding=utf-8
from client.src.mqtt.SUB import Subscriber
import json
import os
from client.src.socket_.Client import Client
from client.src.mqtt.PUB import Publisher

class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = dados
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        connection.request('/config/leitor', self.dados)
        return connection.requestRecv()['headers']

    def testConnection(self):
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))
        connection = self.getConnection()
        connection.request('/test')
        return connection.requestRecv()['headers']
    
    def getConnection(self, i=1):
        if i == 1: return Publisher("node02.myqtthub.com", 1883, "2", "cliente2", "135790")
        else: return Subscriber("node02.myqtthub.com", 1883, "2", "cliente2", "135790")

    def getButton(self):
        connection = self.getConnection(2)
        connection.request('/button')
        return connection.requestRecv()['headers']