
# coding=utf-8
from client.src.socket_.Client import Client
from models.Autorama import Autorama
from models.Leitor import Leitor
from operator import attrgetter
import time

class Classificacao:
    def __init__(self, corrida_id = None):
        self.autorama = Autorama()
        self.leitor = Leitor()
        self.corridaEnd = False
        self.dadosCorrida = None
        self.primeiroVoltas = 0 #quantidade de voltas do primeiro colocado
        self.primeiroTimestamp = 0 #timestamp. tempo de corrida do primeiro colocado
        if(corrida_id == None):
            self.corrida = self.autorama.getCorridaAtual()
        else:
            self.corrida = self.autorama.getCorrida(corrida_id)
        
    
    def save(self):
        self.autorama.saveCorrida(self.corrida)
        
    def classificacao(self):
        connection = self.leitor.getConnection()
        headers = { 'pilotos': self.corrida['pilotos'], 'tempoMinimoVolta': self.autorama.getPista(self.corrida['circuito_id'])['tempoMinimoVolta'] }
        connection.request('/corrida/qualificatoria/carros', 'POST', headers)#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def classificacaoAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.requestOpen('/corrida/qualificatoria/acompanhar', 'GET', '')
        self.corridaEnd = False
        corrida = self.autorama.getCorridaAtual()
        classificacao = corrida['classificacao']
        while not self.corridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da classificacao ) }
            result = connection.requestRecv()#aguarda o leitor responder com uma tag
            pos = classificacao[result['tag']]
            if pos['voltas'] < self.corrida['quantidadeDeVoltas']: # se o primeiro carro não terminou a corrida
                pos['time_total'] = self.autorama.timestampFormat(result['time'])
                if(pos['timestamp'] == 0):
                    lap_time = result['time']
                else:
                    lap_time = result['timestamp'] - pos['timestamp']
                lap_time_s = self.autorama.timestampFormat(lap_time)
                pos['time_total'] = lap_time_s
                if(pos['tempo_menor'] > lap_time_s ):
                    pos['tempo_menor'] = lap_time_s
                    circuito = self.autorama.getPista( corrida['circuito_id'])
                    if( pos['tempo_menor'] < circuito['recorde'] ):
                        piloto = self.autorama.getPiloto(pos['piloto_id'])
                        circuito['recorde'] = pos['tempo_menor']
                        circuito['autor'] = piloto['nome']
                        self.autorama.savePista(circuito)
                
                pos['timestamp'] = result['timestamp']
                pos['voltas'] += 1
                classificacao[result['tag']] = pos
                corrida['classificacao'] = classificacao
                if pos['voltas'] > self.primeiroVoltas:
                    self.primeiroVoltas = pos['voltas']
                    self.primeiroTimestamp = pos['timestamp']
                print(classificacao)
                tempoAposPrimeiro = self.autorama.timestampFormat( (result['time'] - self.primeiroTimestamp) )
                # tempo desde que o primeiro colocado concluiu uma volta
                print(tempoAposPrimeiro)
                if(self.primeiroVoltas >= self.corrida['quantidadeDeVoltas'] and tempoAposPrimeiro > "00:15:000" ):
                    self.corridaEnd = True
                    self.corrida['corridaCompleta'] = 1   #encerrada
                else: 
                    self.corrida['corridaCompleta'] = 2  #sendo realizada
                self.autorama.saveCorrida(corrida)
            connection.requestSend({"success": True, "encerrarCorrida": self.corridaEnd})
        connection.requestClose()
    
    def getDadosClassificacao(self):
        corrida = self.corrida
        classificacao = corrida['classificacao']
        self.dadosCorrida = []
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            pos = classificacao[piloto['carro_epc']]
            posicao = {}
            posicao['carro_epc'] = piloto['carro_epc']
            posicao['nome_piloto'] = pilotoAtual['nome']
            posicao['nome_equipe'] = self.autorama.getEquipe(pilotoAtual['equipe_id'])['nome']
            posicao['cor_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['cor']
            posicao['tempo_corrida'] = pos['tempo_total']
            posicao['tempo_volta'] = pos['tempo_atual']
            posicao['tempo_menor'] = pos['tempo_menor']
            posicao['timestamp'] = pos['timestamp']
            posicao['voltas'] = pos['voltas']
            posicao['pits'] = pos['pits']
            posicao['pos_inicial'] = pos['pos_inicial']
            self.dadosCorrida.append(posicao)
        self.dadosCorrida = sorted(self.dadosCorrida, key=attrgetter('tempo_corrida', 'pos_incial'))
        self.dadosCorrida = sorted(self.dadosCorrida, key=attrgetter('voltas'), True)
        for i x in range(1, len(self.dadosCorrida) - 1 ):
            posAnt = self.dadosCorrida[i-1]
            pos = self.dadosCorrida[i]
            if( pos['voltas'] < posAnt['voltas']):
                pos['tempo_corrida'] = '+' + str(posAnt['voltas'] - pos['voltas']) + ' volta'
                if( posAnt['voltas'] - pos['voltas'] > 1):
                    pos['tempo_corrida'] = pos['tempo_corrida'] + 's'
            else:
                pos['tempo_corrida'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - posAnt['timestamp'])
            self.dadosCorrida[i] = pos
        return self.dadosCorrida
    
    def resetClassificacao(self):
        corrida = self.corrida
        classificacao = corrida['classificacao']
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            pos = classificacao[piloto['carro_epc']]
            pos['tempo_total'] = "99:99:999"
            pos['tempo_atual'] = "99:99:999"
            pos['tempo_menor'] = "99:99:999"
            pos['timestamp'] = 0
            pos['voltas'] = 0
        self.save()