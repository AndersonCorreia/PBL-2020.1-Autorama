
# coding=utf-8
import json
import os

class Carro:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/carro.json"):
        self.fileName = file
    
    def save(self, dados):
        self.dados = dados
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))