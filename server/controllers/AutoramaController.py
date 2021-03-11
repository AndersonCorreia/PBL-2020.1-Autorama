# coding=utf-8
from models.Autorama import Autorama
from mercury_.sensor import *
class AutoramaController:
    
    @staticmethod
    def getAll():
        autorama = Autorama()
        return autorama.dados
    
    @staticmethod
    def getLastTag():
        autorama = Autorama()
        print("ultima tag")
        print(autorama.dados['tags']['last'])
        return autorama.dados['tags']['last']
    
    @staticmethod
    def readTag():
        return read()
    