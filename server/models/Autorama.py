# coding=utf-8
import json
import os
class Autorama:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r').read() )
        self.carros = self.dados['carros']
    
    def save(self):
        open(self.fileName, 'w').write( json.dumps(self.dados, indent=4, ensure_ascii=False, skipkeys=False))

    def setLastTag(self, tag):
        self.dados["tags"]["last"] = tag
        self.save()