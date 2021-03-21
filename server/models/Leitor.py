
# coding=utf-8
import json
import os
class Leitor:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/leitor.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
    
    def save(self, dados):
        self.dados = dados
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False,))