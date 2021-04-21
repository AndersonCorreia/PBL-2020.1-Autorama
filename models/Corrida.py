
# coding=utf-8
from client.src.socket_.Client import Client
from models.Autorama import Autorama
from models.Leitor import Leitor
import time
class Corrida:
    def __init__(self, corrida_id = None):
        self.autorama = Autorama()
        self.leitor = Leitor()
        self.corridaEnd = False
        self.dadosCorrida = None
        if(corrida_id == None):
            self.corrida = self.autorama.getCorridaAtual()
        else:
            self.corrida = self.autorama.getCorrida(corrida_id)
        
    
    def save(self):
        self.autorama.saveCorrida(self.corrida)
        
    def corrida(self):
        connection = self.leitor.getConnection()
        headers = { 'pilotos': self.corrida['pilotos'], 'tempoMinimoVolta': self.autorama.getPista(self.corrida['circuito_id'])['tempoMinimoVolta'] }
        connection.request('/corrida/qualificatoria/carros', 'POST', headers)#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def qualificatoriaAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.requestOpen('/corrida/qualificatoria/acompanhar', 'GET', '')
        self.corridaEnd = False
        corrida = self.autorama.getCorridaAtual()
        qualificatoria = corrida['qualificatoria']
        while not self.corridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da qualificatoria ) }
            result = connection.requestRecv()#aguarda o leitor responder com uma tag
            qualificacao = qualificatoria[result['tag']]
            if(qualificacao['timestamp'] == 0):
                lap_time = result['time']
            else:
                lap_time = result['timestamp'] - qualificacao['timestamp']
            lap_time_s = self.autorama.timestampFormat(lap_time)
            if(qualificacao['tempo_menor'] > lap_time_s ):
                qualificacao['tempo_menor'] = lap_time_s
                qualificacao['tempo_menor_timestamp'] = lap_time
                circuito = self.autorama.getPista( corrida['circuito_id'])
                if( qualificacao['tempo_menor'] < circuito['recorde'] ):
                    piloto = self.autorama.getPiloto(qualificacao['piloto_id'])
                    circuito['recorde'] = qualificacao['tempo_menor']
                    circuito['autor'] = piloto['nome']
                    self.autorama.savePista(circuito)
            
            qualificacao['timestamp'] = result['timestamp']
            qualificacao['voltas'] += 1
            qualificatoria[result['tag']] = qualificacao
            corrida['qualificatoria'] = qualificatoria
            print(qualificatoria)
            tempoPercorrido = self.autorama.timestampFormat((result['time']))# interromper a corrida quando já tiver passado 1 minuto depois do tempo limite
            print(tempoPercorrido)
            print(corrida['qualificatoriaDuracao'])
            if(corrida['qualificatoriaDuracao'] <= tempoPercorrido ):
                self.corridaEnd = True #falta ver como interromper a corrida com o apertar do botão
                self.corrida['qualificatoriaCompleta'] = 1   #encerrada
            else: 
                self.corrida['qualificatoriaCompleta'] = 2  #sendo realizada
            self.autorama.saveCorrida(corrida)
            connection.requestSend({"success": True, "encerrarCorrida": self.corridaEnd})
        connection.requestClose()
    
    def getDadosCorrida(self):
        corrida = self.corrida
        qualificatoria = corrida['qualificatoria']
        self.dadosCorrida = []
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            qualificacao = qualificatoria[piloto['carro_epc']]
            pos = {}
            pos['carro_epc'] = piloto['carro_epc']
            pos['nome_piloto'] = pilotoAtual['nome']
            pos['nome_equipe'] = self.autorama.getEquipe(pilotoAtual['equipe_id'])['nome']
            pos['cor_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['cor']
            pos['tempo_volta'] = qualificacao['tempo_menor']
            pos['timestamp'] = qualificacao['tempo_menor_timestamp']
            pos['voltas'] = qualificacao['voltas']
            self.dadosCorrida.append(pos)
        self.dadosCorrida = sorted(self.dadosCorrida, key=lambda pos: pos['timestamp'])
        return self.dadosCorrida
    
    def resetQualificatoria(self):
        corrida = self.corrida
        qualificatoria = corrida['qualificatoria']
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            qualificacao = qualificatoria[piloto['carro_epc']]
            qualificacao['tempo_menor'] = "99:99:999"
            qualificacao['tempo_menor_timestamp'] = 0
            qualificacao['timestamp'] = 0
            qualificacao['voltas'] = 0
        self.save()