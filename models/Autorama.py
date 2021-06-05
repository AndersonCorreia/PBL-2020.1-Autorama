# coding=utf-8
import json
import os
from client.src.mqtt.PUB import Publisher
class Autorama:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r', encoding="UTF-8").read() )
    
    def save(self):
        try:
            open(self.fileName, 'w', encoding="UTF-8").write( json.dumps(self.dados, indent=4, ensure_ascii=False))
        except Exception as e:
            print("Erro no salvamento do json")

    def addCircuito(self, circuito):
        if int(circuito['circuito_id']) == 0:
            circuito['circuito_id'] =  self.dados['circuitos'][-1]['circuito_id'] + 1 if len(self.dados['circuitos']) > 0 else 1
            self.dados['circuitos'].append(circuito)
            self.save()
            # depois fazer função de update
    def addCorrida(self, corrida, pilotos):
        pilotosDict = []
        qualificatoria = {}
        classificacao = {}
        for piloto in pilotos:
            piloto_id = int(piloto)
            carroEpc = self.getCarroByPiloto(piloto_id)["epc"]
            pilotosDict.append({"piloto_id": piloto_id, "carro_epc": carroEpc})
            qualificatoria[carroEpc] = {
                "piloto_id": piloto_id,
                "carro_epc": carroEpc,
                "tempo_menor": "9:99:999",
                "timestamp": 0,
                "voltas": 0
            }
            classificacao[carroEpc] = {
                "piloto_id": piloto_id,
                "carro_epc": carroEpc,
                "tempo_total": "9:99:999",
                "tempo_menor": "9:99:999",
                "tempo_atual": "9:99:999",
                "timestamp": 0,
                "voltas": 0,
                "pits": 0,
                "pos_inicial": 0
            }
        corrida['qualificatoriaCompleta']=0  # não realizada
        corrida['corridaCompleta']=0
        corrida['pilotos'] = pilotosDict
        corrida['qualificatoria'] = qualificatoria
        corrida['classificacao'] = classificacao
        corrida['classificacaoDuracao']="00:00:00"
        if int(corrida['corrida_id']) == 0:
            corrida['circuito_id'] = int(corrida['circuito_id'])
            corrida['quantidadeDeVoltas'] = int(corrida['quantidadeDeVoltas'])
            corrida['corrida_id'] = self.dados['corridas'][-1]['corrida_id'] + 1 if len(self.dados['corridas']) > 0 else 1 #autoincremento
            corrida.pop('piloto_id[]', '')
            self.dados['corridas'].append(corrida)
            self.save()
    
    def setCorridaAtiva(self, dados):
        self.dados['corrida_ativa'] = int(dados['corrida_ativa'])
        self.save()
        pub = self.getConnection()
        corrida = self.getCorridaAtual()
        dados = { 'corrida': self.getCorridaAtual(), 'circuito': self.getPista(corrida['circuito_id'])}
        pub.request('/acompanhar/corrida/atual', dados, True, False)

    def getCorridas(self):
        corridas = self.dados['corridas']
        for corrida in corridas:
            corrida['circuito'] = self.getPista(corrida['circuito_id'])
        return corridas

    def getCorridaAtual(self):
        return self.getCorrida(self.dados['corrida_ativa'])
            
    def getCorrida(self, corrida_id):
        for corrida in self.dados['corridas']:
            if corrida['corrida_id'] == corrida_id:
                return corrida
            
    def saveCorrida(self, corridaUpdate):
        corridas = []
        for corrida in self.dados['corridas']:
            if corrida['corrida_id'] == corridaUpdate['corrida_id']:
                corridas.append(corridaUpdate)
            else :
                corridas.append(corrida)
        self.dados['corridas'] = corridas
        self.save()

    def getPista(self, pista_id):
        for pista in self.dados['circuitos']:
            if pista['circuito_id'] == pista_id:
                return pista

    def savePista(self, circuitoUpdate):
        circuitos = []
        for circuito in self.dados['circuitos']:
            if circuito['circuito_id'] == circuitoUpdate['circuito_id']:
                circuitos.append(circuitoUpdate)
            else :
                circuitos.append(circuito)
        self.dados['circuitos'] = circuitos
        self.save()
    
    def addPiloto(self, piloto):
        piloto['piloto_id'] = int(piloto['piloto_id'])
        if piloto['piloto_id'] == 0:
            piloto['carro_id'] = int(piloto['carro_id'])
            piloto['equipe_id'] = int(piloto['equipe_id'])
            piloto['piloto_id'] = self.dados['pilotos'][-1]['piloto_id'] + 1 if len(self.dados['pilotos']) > 0 else 1
            piloto['ativo']=True
            self.dados['pilotos'].append(piloto)
            self.save()

    def addEquipe(self, equipe):
        equipe['equipe_id'] = int(equipe['equipe_id'])
        if equipe['equipe_id'] == 0:
            equipe['equipe_id'] = self.dados['equipes'][-1]['equipe_id'] + 1 if len(self.dados['equipes']) > 0 else 1
            equipe['pontos'] = 0
            self.dados['equipes'].append(equipe)
            self.save()

    def getCarroByPiloto(self, piloto_id):
        piloto = self.getPiloto(piloto_id)
        return self.getCarro(piloto['carro_id'])
            
    def getCarro(self, carro_id):
        for carro in self.dados['carros']:
            if carro['carro_id'] == carro_id:
                return carro
            
    def getPiloto(self, piloto_id):
        for piloto in self.dados['pilotos']:
            if piloto['piloto_id'] == piloto_id:
                return piloto
    
    def getEquipe(self, equipe_id):
        for equipe in self.dados['equipes']:
            if equipe['equipe_id'] == equipe_id:
                return equipe
            
    def timestampFormat(self, time):
        minutos = str( int(time/60) )
        if( len(minutos) == 1):
            minutos = "0" + minutos
        
        segundos = str( int(time%60))
        if( len(segundos) == 1):
            segundos = "0" + segundos
        
        milisegundos = str( float(time%1))
        milisegundos = milisegundos[2:5]
        return "" + minutos + ":" + segundos  + ":" + milisegundos
    
    def getConnection(self):
        return Publisher("node02.myqtthub.com", 1883, "cliente", "cliente", "cliente")
        # return Publisher("node02.myqtthub.com", 1883, "2", "cliente2", "135790")