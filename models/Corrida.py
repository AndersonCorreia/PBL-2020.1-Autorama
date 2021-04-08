
# coding=utf-8
from client.src.socket_.Client import Client
from models.Autorama import Autorama
from models.Leitor import Leitor
import time
class Corrida:
    def __init__(self, corrida_id):
        self.autorama = Autorama()
        self.leitor = Leitor()
        self.corrida = self.autoram.getCorrida(corrida_id)
    
    def save(self, dados):
        self.autoram.saveCorrida(self.corrida)
        
    def qualificatoria(self):
        connection = self.leitor.getConnection()
        connection.request('/corrida/qualificatoria/carros', 'POST', self.corrida['pilotos'])#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def qualificatoriaAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.requestOpen('/corrida/qualificatoria/acompanhar', 'GET', '')
        corridaEnd = False
        corrida = self.autorama.getCorridaAtual()
        qualificatoria = corrida['qualificatoria']
        while not CorridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da qualificatoria ) }
            result = connection.requestRecv()#aguarda o leitor responder com uma tag
            qualificacao = qualificatoria[result['tag']]
            if(qualificacao['timestamp'] == 0){
                qualificacao['tempo_menor'] = result['time']
            }
            else {
                qualificacao['tempo_menor'] = result['timestamp'] - qualificacao['timestamp']
            }
            qualificacao['timestamp'] = result['timestamp']
            qualificacao['voltas'] += 1
            qualificatoria[result['tag']] = qualificacao
            corrida['qualificatoria'] = qualificatoria
            self.autorama.saveCorrida(corrida)
            timeForEnd = self.autorama.timestampFormat(result['time'] - 60)# interromper a corrida quando já tiver passado 1 minuto depois do tempo limite
            if(qualificatoria['qualificatoriaDuracao'] < timeForEnd ):
                corridaEnd == True #falta ver como interromper a corrida com o apertar do botão
                
            connection.requestSend({"success": True, "encerrarCorrida": corridaEnd})
        connection.requestClose