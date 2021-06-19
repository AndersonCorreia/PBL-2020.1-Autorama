
# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
from operator import itemgetter
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
        connection.request('/corrida/carros', headers)#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def classificacaoAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.request('/corrida/acompanhar', '')
        self.corridaEnd = False
        classificacao = self.corrida['classificacao']
        while not self.corridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da classificacao ) }
            print('sub')
            result = connection.requestRecv(False)['headers']#aguarda o leitor responder com uma tag
            print('sub-end')
            if 'tag' in result:
                pos = classificacao[result['tag']]
                if pos['voltas'] < self.corrida['quantidadeDeVoltas']: # se o primeiro carro não terminou a corrida
                    pos['tempo_total'] = self.autorama.timestampFormat(result['time'])
                    if(pos['timestamp'] == 0):
                        lap_time = result['time']
                    else:
                        lap_time = result['timestamp'] - pos['timestamp']
                    lap_time_s = self.autorama.timestampFormat(lap_time)
                    pos['tempo_atual'] = lap_time_s
                    if(pos['tempo_menor'] > lap_time_s ):
                        pos['tempo_menor'] = lap_time_s
                        circuito = self.autorama.getPista( self.corrida['circuito_id'])
                        if( pos['tempo_menor'] < circuito['recorde'] ):
                            piloto = self.autorama.getPiloto(pos['piloto_id'])
                            circuito['recorde'] = pos['tempo_menor']
                            circuito['autor'] = piloto['nome']
                            self.autorama.savePista(circuito)
                    
                    pos['timestamp'] = result['timestamp']
                    pos['voltas'] += 1
                    classificacao[result['tag']] = pos
                    self.corrida['classificacao'] = classificacao
                    if pos['voltas'] > self.primeiroVoltas:
                        self.primeiroVoltas = pos['voltas']
                        self.primeiroTimestamp = pos['timestamp']
                    print(classificacao)
                tempoAposPrimeiro = self.autorama.timestampFormat( (result['timestamp'] - self.primeiroTimestamp) )
                # tempo desde que o primeiro colocado concluiu uma volta
                print(tempoAposPrimeiro)
                if(self.primeiroVoltas >= self.corrida['quantidadeDeVoltas'] and tempoAposPrimeiro > "00:15:000" or self.corridaEnd ):
                    self.corridaEnd = True
                    self.corrida['corridaCompleta'] = 1   #encerrada
                else: 
                    self.corrida['corridaCompleta'] = 2  #sendo realizada
                self.save()
                self.publicarDadosClassificacao(result['tag'], connection)
        connection.request('/corrida/encerrar')
    
    def publicarDadosClassificacao(self, tag, pub):
        self.getDadosClassificacao()
        pub.request('/corrida/acompanhar/' + str(self.corrida['corrida_id']), self.dadosCorrida, True, False, False)
        for piloto in self.dadosCorrida:
            if piloto['carro_epc'] == tag:
                pub.request('/corrida/acompanhar/' + str(self.corrida['corrida_id']) + '/piloto/' + tag, piloto, True, False, False)
                break
                
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
            posicao['num_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['num']
            posicao['tempo_corrida'] = pos['tempo_total']
            posicao['tempo_volta'] = pos['tempo_atual']
            posicao['tempo_menor'] = pos['tempo_menor']
            posicao['timestamp'] = pos['timestamp']
            posicao['voltas'] = pos['voltas']
            posicao['pits'] = pos['pits']
            posicao['pos_inicial'] = pos['pos_inicial']
            self.dadosCorrida.append(posicao)
        self.dadosCorrida = sorted(self.dadosCorrida, key=itemgetter('tempo_corrida', 'pos_inicial'))
        self.dadosCorrida = sorted(self.dadosCorrida, key=itemgetter('voltas'), reverse=True)
        self.dadosCorrida[0]['posicao'] = 1
        self.posicaoEntrePilotos(self.dadosCorrida[0], None, self.dadosCorrida[1])
        for i in range(1, len(self.dadosCorrida) ):
            posPrimeiro = self.dadosCorrida[0]
            pos = self.dadosCorrida[i]
            pos['posicao'] = i+1
            if( pos['voltas'] < posPrimeiro['voltas']):
                pos['tempo_corrida'] = '+' + str(posPrimeiro['voltas'] - pos['voltas']) + ' volta'
                if( posPrimeiro['voltas'] - pos['voltas'] > 1):
                    pos['tempo_corrida'] = pos['tempo_corrida'] + 's'
            else:
                pos['tempo_corrida'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - posPrimeiro['timestamp'])
            if i == (len(self.dadosCorrida) - 1):
                self.posicaoEntrePilotos(pos, self.dadosCorrida[i-1])
            else:
                self.posicaoEntrePilotos(pos, self.dadosCorrida[i-1], self.dadosCorrida[i+1] )
            self.dadosCorrida[i] = pos
        return self.dadosCorrida
    
    def posicaoEntrePilotos(self, pos, proximo=None, anterior=None):
        pos['piloto_proximo'] = False
        pos['piloto_anterior'] = False
        if proximo:
            pos['piloto_proximo'] = proximo['nome_piloto']
            pos['num_proximo'] = proximo['num_carro']
            if( pos['voltas'] < proximo['voltas']):
                pos['tempo_proximo'] = '+' + str(proximo['voltas'] - pos['voltas']) + ' volta'
                if( proximo['voltas'] - pos['voltas'] > 1):
                    pos['tempo_proximo'] = pos['tempo_proximo'] + 's'
            else:
                pos['tempo_proximo'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - proximo['timestamp'])
            
        if anterior:
            pos['piloto_anterior'] = anterior['nome_piloto']
            pos['num_anterior'] = anterior['num_carro']
            if( pos['voltas'] > anterior['voltas']):
                pos['tempo_anterior'] = '+' + str( pos['voltas'] - anterior['voltas']) + ' volta'
                if(  pos['voltas'] - anterior['voltas'] > 1):
                    pos['tempo_anterior'] = pos['tempo_anterior'] + 's'
            else:
                pos['tempo_anterior'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - anterior['timestamp'])
    
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

    def setTime(self, time):
        self.corrida['classificacaoDuracao'] = time
        self.save()