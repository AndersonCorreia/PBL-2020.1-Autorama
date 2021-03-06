# coding=utf-8
from models.autorama import Autorama

class AutoramaController:
    
    @staticmethod
    def getAll():
        autorama = Autorama()
        return autorama.dados
    
    @staticmethod
    def getLastTag():
        autorama = Autorama()
        return autorama.dados['tags']['last']
    