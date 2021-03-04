# coding=utf-8
import json

class Autorama:
    def __init__(self, file="autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
        self.carros = self.dados['carros']
    
    def save(self):
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))