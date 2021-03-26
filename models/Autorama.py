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
        for piloto in pilotos:
            pilotosDict.append({"piloto_id": int(piloto)})
        corrida['pilotos'] = pilotosDict
        if int(corrida['corrida_id']) == 0:
            corrida['circuito_id'] = int(corrida['circuito_id'])
            corrida['quantidadeDeVoltas'] = int(corrida['quantidadeDeVoltas'])
            corrida['qualificatoria'] = []
            corrida['classificacao'] = []
            corrida['corrida_id'] = self.dados['corridas'][-1]['corrida_id'] + 1
            corrida.pop('piloto_id[]', '')
            self.dados['corridas'].append(corrida)
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
