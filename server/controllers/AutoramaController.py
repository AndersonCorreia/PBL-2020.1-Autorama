# coding=utf-8
from models.Autorama import Autorama
import mercury_.sensor
class AutoramaController:
    
    @staticmethod
    def getAll():
        autorama = Autorama()
        return autorama.dados
    
    @staticmethod
    def getLastTag():
        autorama = Autorama()
        return autorama.dados['tags']['last']
    
    @staticmethod
    def readTag():
        return read()
    