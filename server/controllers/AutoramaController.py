# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
from mercury_.sensor import *
class AutoramaController:
    
    @staticmethod
    def getAll():
        autorama = Autorama()
        return autorama.dados

    @staticmethod
    def setConfigLeitor(dados):
        leitor = Leitor()
        leitor.save(dados)
    
    @staticmethod
    def readTag():
        return read()
    
    @staticmethod
    def definirTagsParaLeitura(headers):
        tags = []
        while( len(headers['pilotos']) > 0 ):
                piloto = headers['pilotos'].pop(0)
                tags.insert(piloto['carro_epc'])
        setTagsForRead(tags)
    