# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
from mercury_.sensor import *
from controllers.SensorThread import SensorThread
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
            tags.append(piloto['carro_epc'])
        setTagsForRead(tags, headers['tempoMinimoVolta'])
        return {'success': True, 'dados': []}
    
    @staticmethod  
    def qualificatoria(headers, pub):
        log = loadLog()
        # sensorTRead = SensorThread(pub, log, 'read')
        # sensorTRead.start()
        sensorTSend = SensorThread(pub, log, 'send')
        sensorTSend.start()
        sensorTEncerrar = SensorThread(pub, log, 'encerrar')
        sensorTEncerrar.start()
        return {'success': True, 'dados': []}
    
    @staticmethod
    def setLogTimestamp():
        setLogTimestampInicial()
    