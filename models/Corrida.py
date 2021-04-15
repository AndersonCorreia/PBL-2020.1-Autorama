
# coding=utf-8
from client.src.socket_.Client import Client
from models.Autorama import Autorama
from models.Leitor import Leitor
import time
class Corrida:
    def __init__(self, corrida_id = None):
        self.autorama = Autorama()
        self.leitor = Leitor()
        if(corrida_id == None):
            self.corrida = self.autorama.getCorridaAtual()
            self.dadosQualificatoria = []
        else:
            self.corrida = self.autorama.getCorrida(corrida_id)
            self.dadosQualificatoria = self.addDadosQualificatoria()
    
    def save(self, dados):
        self.autorama.saveCorrida(self.corrida)
        
    def qualificatoria(self):
        connection = self.leitor.getConnection()
        headers = { 'pilotos': self.corrida['pilotos'], 'tempoMinimoVolta': self.autorama.getPista(self.corrida['circuito_id'])['tempoMinimoVolta'] }
        connection.request('/corrida/qualificatoria/carros', 'POST', headers)#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def qualificatoriaAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.requestOpen('/corrida/qualificatoria/acompanhar', 'GET', '')
        corridaEnd = False
        corrida = self.autorama.getCorridaAtual()
        qualificatoria = corrida['qualificatoria']
        while not corridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da qualificatoria ) }
            result = connection.requestRecv()#aguarda o leitor responder com uma tag
            qualificacao = qualificatoria[result['tag']]
            if(qualificacao['timestamp'] == 0):
                qualificacao['tempo_menor'] = result['time']
        
            else:
                qualificacao['tempo_menor'] = result['timestamp'] - qualificacao['timestamp']
            
            qualificacao['timestamp'] = result['timestamp']
            qualificacao['voltas'] += 1
            qualificatoria[result['tag']] = qualificacao
            corrida['qualificatoria'] = qualificatoria
            self.autorama.saveCorrida(corrida)
            self.updateDadosQualificatoria(result['tag'])
            print(qualificatoria)
            tempoPercorrido = self.autorama.timestampFormat((result['time'] - 60))# interromper a corrida quando já tiver passado 1 minuto depois do tempo limite
            print(tempoPercorrido)
            if(corrida['qualificatoriaDuracao'] < tempoPercorrido ):
                corridaEnd == True #falta ver como interromper a corrida com o apertar do botão
                
            connection.requestSend({"success": True, "encerrarCorrida": corridaEnd})
        connection.requestClose()
    
    def getDadosQualificatoria(self):
        return self.dadosQualificatoria

    def addDadosQualificatoria(self):
        corrida = self.corrida
        qualificatoria = corrida['qualificatoria']
        i=0
        dadosQualificatoria = []
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            qualificacao = qualificatoria[piloto['carro_epc']]
            pos = {}
            i=i+1
            pos['pos'] = i
            pos['carro_epc'] = piloto['carro_epc']
            pos['nome_piloto'] = pilotoAtual['nome']
            pos['nome_equipe'] = self.autorama.getEquipe(pilotoAtual['equipe_id'])['nome']
            pos['cor_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['cor']
            pos['tempo_volta'] = qualificacao['tempo_menor']
            pos['voltas'] = qualificacao['voltas']
            dadosQualificatoria.append(pos)
        return dadosQualificatoria 

    def updateDadosQualificatoria(self, tag):
        corrida = self.corrida
        qualificatoria = corrida['qualificatoria']

        for pos in self.dadosQualificatoria:
            if pos['carro_epc'] == tag:
                qualificacao = qualificatoria[pos['carro_epc']]
                pos['tempo_volta'] = qualificacao['tempo_menor']
                pos['voltas'] = qualificacao['voltas']
        sorted(dadosQualificatoria, key=lambda pos: pos['tempo_volta'])