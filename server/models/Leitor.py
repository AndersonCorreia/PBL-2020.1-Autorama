
# coding=utf-8
import json
import os
class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = json.loads(dados)
        open(self.fileName, 'w').write(dados)

    def getDados(self):
        return self.dados