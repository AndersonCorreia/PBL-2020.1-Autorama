# coding=utf-8
import json
import os
from client.src.mqtt.PUB import Publisher
# Arquivo de configurações com informações do servidor broker MQTT
configFile=os.path.dirname(os.path.realpath(__file__))+"/config.json"
CONFIG = json.loads(open(configFile, 'r').read())
class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = dados 
        dado_str = json.dumps(dados, indent=4, ensure_ascii=False,)
        open(self.fileName, 'w').write( dado_str )
        connection = self.getConnection()
        connection.request('/config/leitor', dado_str)
        return connection.requestRecv()['headers']

    def testConnection(self):
        connection = self.getConnection()
        connection.request('/test')
        return connection.requestRecv()['headers']
    
    def getConnection(self):
        return Publisher(CONFIG['host'], CONFIG['port'], CONFIG['id'], CONFIG['username'], CONFIG['password'])

    def getButton(self):
        connection = self.getConnection()
        connection.request('/button')
        return connection.requestRecv()['headers']