# coding=utf-8
import json
import os
import time
import random
from client.src.mqtt.SUB import Subscriber

class Autorama:
    def __init__(self, isQualificatoria=True, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        if open(file, 'r', encoding="UTF-8").read() == "":
            open(file, 'w', encoding="UTF-8").write('{"corrida_ativa": false}')
        self.dados = json.loads(open(file, 'r', encoding="UTF-8").read() )
        self.isQualificatoria=isQualificatoria

    def save(self):
        try:
            open(self.fileName, 'w', encoding="UTF-8").write( json.dumps(self.dados, indent=4, ensure_ascii=False))
        except Exception as e:
            print("Erro no salvamento do json")

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
        return Subscriber("node02.myqtthub.com", 1883, "usuario", "usuario", "usuario")
        #return Subscriber("node02.myqtthub.com", 1883, "usuario1", "usuario", "usuario")
        
    def updateCorridaAtual(self, force = False):
        connection = self.getConnection()
        atualizado = False
        connection.request('/corrida/acompanhar/atual')
        while( not atualizado):
            time.sleep(2)
            corrida = connection.requestRecv(False).payload
            status = self.getStatusCorrida()
            if self.dados['corrida']['corrida_id'] != corrida['corrida']['corrida_id'] or force:
                atualizado = True
                self.dados['corrida'] = corrida['corrida']
                self.dados['corrida']['qualificatoria'] = []
                self.dados['corrida']['classificacao'] = []
                self.dados['corrida']['acompanhar'] = {}
                for piloto in self.dados['corrida']['pilotos']:
                    self.dados['corrida']['acompanhar'][piloto['carro_epc']] = {}
                self.dados['circuito'] = corrida['circuito']
                self.dados['pilotos'] = corrida['pilotos']
                self.dados['equipes'] = corrida['equipes']
                self.dados['carros'] = corrida['carros']
                self.dados['corrida_ativa'] = True
                self.save()
        # connection.disconnect()
        return {'atualizado': atualizado }
        
    def getStatusCorrida(self):
        if self.isQualificatoria:
            return self.dados['corrida']['qualificatoriaCompleta']
        else:
            return self.dados['corrida']['corridaCompleta']
    
    def getDataPilot(self, tag):
        '''print(self.isQualificatoria)
        if self.isQualificatoria:
            corrida = self.dados['corrida']['qualificatoria']
        else: 
            corrida = self.dados['corrida']['classificacao']
        for dado in corrida:
            if dado['carro_epc'] == tag:
                return dado
        '''
        return self.dados['corrida']['acompanhar'][tag]
    
    def getDadosCorrida(self, classificação = True):
        if classificação:
            return self.dados['corrida']['classificacao']
        return self.dados['corrida']['qualificatoria']
    
    #realiza a inscrição para acompanhar dados de um piloto
    def getDataPilotMqtt(self, id):
        piloto = self.getPiloto(id)
        tag = piloto['carro_epc']
        sub = self.getConnection()
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/piloto/' + tag)
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/classificacao/status')
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/qualificatoria/status')
        while True:
            dados = sub.requestRecv(False)
            if dados.topic == '/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/classificacao/status':
                self.dados['corrida']['corridaCompleta'] = dados.payload
                self.isQualificatoria = False
            elif dados.topic == '/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/qualificatoria/status':
                self.dados['corrida']['qualificatoriaCompleta'] = dados.payload
                self.isQualificatoria = True
            else:
                print("acompanhar ", dados.payload)
                self.dados['corrida']['acompanhar'][tag] = dados.payload
            self.save()
    
    def getDadosCorridaMqtt(self, classificação = True):
        sub = self.getConnection()
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']))
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/classificacao/status')
        sub.request('/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/qualificatoria/status')
        while True:
            dados = sub.requestRecv(False)
            print("topic: ", dados.topic)
            if dados.topic == '/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/classificacao/status':
                self.dados['corrida']['corridaCompleta'] = dados.payload
                self.isQualificatoria = False
            elif dados.topic == '/corrida/acompanhar/' + str(self.dados['corrida']['corrida_id']) + '/qualificatoria/status':
                self.dados['corrida']['qualificatoriaCompleta'] = dados.payload
                self.isQualificatoria = True
            else:
                print("classificaçao: ", classificação)
                if classificação:
                    self.dados['corrida']['classificacao'] = dados.payload
                else: 
                    self.dados['corrida']['qualificatoria'] = dados.payload
            self.save()
      
    #retorna os dados necessários para a tela de acompanhar piloto    
    def showPilot(self, id):
        piloto = self.getPiloto(id)
        carro = self.getCarro(piloto['carro_id'])
        equipe = self.getEquipe(piloto['equipe_id'])
        logos = ['logo_1.png', 'logo_2.png', 'logo_3.png']
        fotos = ['foto_1.jpg']
        bandeiras = ['bandeira_1.jpg']
        dados=[]
        if self.dados['corrida_ativa']:
            dados = self.getDataPilot(carro['epc'])
            print("dado1 ", dados)
            dados['bandeira_piloto'] = "/static/img/pilotos/" + random.choice(bandeiras)   
            dados['foto_piloto'] = "/static/img/pilotos/" + random.choice(fotos)
            dados['logo_equipe'] = "/static/img/equipes/logo_" + str(equipe['equipe_id'])+".png"
        else:
            dados = {
                'piloto_id': piloto['piloto_id'],
                'nome_piloto': piloto['nome'],
                'apelido_piloto': piloto['apelido'],
                'bandeira_piloto': "/static/img/pilotos/" + random.choice(bandeiras),
                'foto_piloto': "/static/img/pilotos/" + random.choice(fotos),
                'num_carro': carro['num'],
                'nome_equipe': equipe['nome'],
                'logo_equipe': "/static/img/equipes/logo_" + str(equipe['equipe_id'])+".png"
            }
        return dados