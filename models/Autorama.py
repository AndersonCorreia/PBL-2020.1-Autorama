# coding=utf-8
import json
import os
class Autorama:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r', encoding="UTF-8").read() )
    
    def save(self):
        open(self.fileName, 'w', encoding="UTF-8").write( json.dumps(self.dados, indent=4, ensure_ascii=False))

    def addCircuito(self, circuito):
        if int(circuito['circuito_id']) == 0:
            circuito['circuito_id'] = self.dados['circuitos'][-1]['circuito_id'] + 1
            self.dados['circuitos'].append(circuito)
            self.save()
            # depois fazer função de update
    def addCorrida(self, corrida, pilotos):
        pilotosDict = []
        qualificatoria = []
        classificacao = []
        for piloto in pilotos:
            piloto_id = int(piloto)
            carroEpc = self.getCarroByPiloto(piloto_id)["epc"]
            pilotosDict.append({"piloto_id": piloto_id, "carro_epc": carroEpc})
            qualificatoria.[carroEpc] = {
                "piloto_id": piloto_id,
                "carro_epc": carroEpc,
                "tempo_menor": "9:99:999",
                "timestamp": 0,
                "voltas": 0
            })
            classificacao.[carroEpc] = {
                "piloto_id": piloto_id,
                "carro_epc": carroEpc,
                "tempo_total": "9:99:999",
                "tempo_menor": "9:99:999",
                "tempo_atual": "9:99:999",
                "timestamp": 0,
                "voltas": 0,
                "pits": 0
            })
        corrida['pilotos'] = pilotosDict
        corrida['qualificatoria'] = qualificatoria
        corrida['classificacao'] = classificacao
        if int(corrida['corrida_id']) == 0:
            corrida['circuito_id'] = int(corrida['circuito_id'])
            corrida['quantidadeDeVoltas'] = int(corrida['quantidadeDeVoltas'])
            corrida['corrida_id'] = self.dados['corridas'][-1]['corrida_id'] + 1 #autoincremento
            corrida.pop('piloto_id[]', '')
            self.dados['corridas'].append(corrida)
            self.save()
    
    def setCorridaAtiva(self, dados):
        self.dados['corrida_ativa'] = int(dados['corrida_ativa'])
        self.save()

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
        Corridas = []
        for corrida in self.dados['corridas']:
            if corrida['corrida_id'] == corridaUpdate['corrida_id']:
                corridas.append(corridaUpdate)
            else :
                corridas.append(corrida)
        self.dados['corridas'] = Corridas
        self.save()

    def getPista(self, pista_id):
        for pista in self.dados['circuitos']:
            if pista['circuito_id'] == pista_id:
                return pista

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
            
    def timestampFormat(time):
        return "" + str( int(time/60) ) + ":" + str(time%60) + ":000"