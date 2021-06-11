# coding=utf-8
from models.usuario.Autorama import Autorama as AutoramaUser
from operator import itemgetter
import time

class Classificacao:
    def __init__(self):
        self.autorama = AutoramaUser()
        self.corridaEnd = False
        self.dadosCorrida = None
        self.primeiroVoltas = 0 #quantidade de voltas do primeiro colocado
        self.primeiroTimestamp = 0 #timestamp. tempo de corrida do primeiro colocado
        self.corrida = self.autorama.dados['corrida']
    
    def save(self):
        self.autorama.dados['corrida'] = self.corrida
        
    def getDadosClassificacao(self):
        return self.autorama.getDadosClassificacao()