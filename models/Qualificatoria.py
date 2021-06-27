
# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
import time
class Qualificatoria:
    def __init__(self, corrida_id = None):
        self.autorama = Autorama()
        self.leitor = Leitor()
        self.corridaEnd = False
        self.dadosQualificatoria = None
        if(corrida_id == None):
            self.corrida = self.autorama.getCorridaAtual()
        else:
            self.corrida = self.autorama.getCorrida(corrida_id)
        
    
    def save(self):
        self.autorama.saveCorrida(self.corrida)
        
    def qualificatoria(self):
        connection = self.leitor.getConnection()
        headers = { 'pilotos': self.corrida['pilotos'], 'tempoMinimoVolta': self.autorama.getPista(self.corrida['circuito_id'])['tempoMinimoVolta'] }
        connection.request('/corrida/carros',headers)#informa ao leitor quais as tags que devem ser lidas
        
    #o codigo abaixo deve ser executado em uma thread separada
    def qualificatoriaAcompanhar(self):
        connection = self.leitor.getConnection()
        connection.request('/corrida/acompanhar', '')
        self.corridaEnd = False
        corrida = self.autorama.getCorridaAtual()
        qualificatoria = corrida['qualificatoria']
        subscriber = True # variavel para determinar se um subscriber deve ser enviadado para acompanhar a corrida, se inscrevendo apenas uma vez na rota
        while not self.corridaEnd:
            # result = {"tag": epc , "timestamp": timestamp, "time": timestamp desde o inicio da qualificatoria ) }
            result = connection.requestRecv(False, subscriber)['headers']#aguarda o leitor responder com uma tag
            subscriber = False
            if 'tag' in result:
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
                if(corrida['qualificatoriaDuracao'] <= tempoPercorrido or self.corridaEnd):
                    self.corridaEnd = True
                    self.corrida['qualificatoriaCompleta'] = 1   #encerrada
                else: 
                    self.corrida['qualificatoriaCompleta'] = 2  #sendo realizada
                self.save()
                self.publicarDadosQualificatoria(result['tag'], self.corridaEnd, connection)
        connection.request('/corrida/encerrar')
        self.autorama.setCorridaAtiva()
        self.setPosInicialForCorrida()
        
    def publicarDadosQualificatoria(self, tag, status, pub):
        self.getDadosQualificatoria()
        print(self.corrida['qualificatoriaCompleta'])
        pub.request('/corrida/acompanhar/' + str(self.corrida['corrida_id']) + "/qualificatoria/status", status, False, False, False)
        pub.request('/corrida/acompanhar/' + str(self.corrida['corrida_id']), self.dadosQualificatoria, True, False, False)
        for piloto in self.dadosQualificatoria:
            if piloto['carro_epc'] == tag:
                pub.request('/corrida/acompanhar/' + str(self.corrida['corrida_id']) + '/piloto/' + tag, piloto, True, False, False)
                break
    
    def getDadosQualificatoria(self):
        corrida = self.corrida
        qualificatoria = corrida['qualificatoria']
        self.dadosQualificatoria = []
        for piloto in corrida['pilotos']:
            pilotoAtual = self.autorama.getPiloto(piloto['piloto_id'])
            qualificacao = qualificatoria[piloto['carro_epc']]
            pos = {}
            pos['carro_epc'] = piloto['carro_epc']
            pos['nome_piloto'] = pilotoAtual['nome']
            pos['nome_equipe'] = self.autorama.getEquipe(pilotoAtual['equipe_id'])['nome']
            pos['cor_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['cor']
            pos['num_carro'] = self.autorama.getCarro(pilotoAtual['carro_id'])['num']
            pos['tempo_volta'] = qualificacao['tempo_menor']
            pos['timestamp'] = qualificacao['tempo_menor_timestamp']
            pos['voltas'] = qualificacao['voltas']
            self.dadosQualificatoria.append(pos)
        self.dadosQualificatoria = sorted(self.dadosQualificatoria, key=lambda pos: pos['timestamp'])
        self.dadosQualificatoria[0]['posicao'] = 1
        self.posicaoEntrePilotos(self.dadosQualificatoria[0], None, self.dadosQualificatoria[1])
        for i in range(1, len(self.dadosQualificatoria) ):
            posPrimeiro = self.dadosQualificatoria[0]
            pos = self.dadosQualificatoria[i]
            pos['posicao'] = i+1
            pos['tempo_corrida'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - posPrimeiro['timestamp'])
            if i == (len(self.dadosQualificatoria) - 1):
                self.posicaoEntrePilotos(pos, self.dadosQualificatoria[i-1])
            else:
                self.posicaoEntrePilotos(pos, self.dadosQualificatoria[i-1], self.dadosQualificatoria[i+1] )
            self.dadosQualificatoria[i] = pos
        return self.dadosQualificatoria
    
    def posicaoEntrePilotos(self, pos, proximo=None, anterior=None):
        pos['piloto_proximo'] = False
        pos['piloto_anterior'] = False
        if proximo:
            pos['piloto_proximo'] = proximo['nome_piloto']
            pos['num_proximo'] = proximo['num_carro']
            pos['tempo_proximo'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - proximo['timestamp'])
            
        if anterior:
            pos['piloto_anterior'] = anterior['nome_piloto']
            pos['num_anterior'] = anterior['num_carro']
            pos['tempo_anterior'] = "+" + self.autorama.timestampFormat( pos['timestamp'] - anterior['timestamp'])
    
    def setPosInicialForCorrida(self):
        self.getDadosQualificatoria()
        pos = 1
        for piloto in self.dadosQualificatoria:
            self.corrida["classificacao"][piloto['carro_epc']]['pos_inicial'] = pos
            pos = pos + 1
        self.save()
    
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