# coding=utf-8
import json
import os
import time
import random
from client.src.mqtt.SUB import Subscriber

class Autorama:
    def __init__(self, file=os.path.dirname(os.path.realpath(__file__))+"/autorama.json"):
        self.fileName = file
        self.dados = json.loads(open(file, 'r', encoding="UTF-8").read() )
    
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
        # return Subscriber("node02.myqtthub.com", 1883, "2", "cliente2", "135790")
        
    def updateCorridaAtual(self, force = False):
        connection = self.getConnection()
        atualizado = False
        connection.request('/acompanhar/corrida/atual')
        while( not atualizado):
            time.sleep(2)
            corrida = connection.requestRecv(False).payload
            if self.dados['corrida']['corrida_id'] != corrida['corrida']['corrida_id'] or force:
                atualizado = True
                self.dados['corrida'] = corrida['corrida']
                self.dados['circuito'] = corrida['circuito']
                self.dados['pilotos'] = corrida['pilotos']
                self.dados['equipes'] = corrida['equipes']
                self.dados['carros'] = corrida['carros']
                self.dados['corrida_ativa'] = True
                self.save()
        return {'atualizado': atualizado }
        
    def getStatusCorrida(self):
        return self.dados['corrida_ativa']

    #realiza a inscrição para acompanhar dados de um piloto
    def getDataPilot(self, tag):
        sub = self.getConnection()
        sub.request('/acompanhar/corrida/' + str(self.dados['corrida']['corrida_id']) + '/piloto/' + tag)
        dados = sub.requestRecv().payload
        return dados
    
    #realiza a inscrição para acompanhar dados de um piloto
    def getDadosClassificacao(self):
        sub = self.getConnection()
        sub.request('/acompanhar/corrida/' + str(self.dados['corrida']['corrida_id']))
        dados = sub.requestRecv().payload
        return dados
            
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
            dados['bandeira_piloto'] = "/static/img/pilotos/" + random.choice(bandeiras)   
            dados['foto_piloto'] = "/static/img/pilotos/" + random.choice(fotos)
            dados['logo_equipe'] = "/static/img/equipes/" + random.choice(logos)
        else:
            dados = {
                'nome_piloto': piloto['nome'],
                'apelido_piloto': piloto['apelido'],
                'bandeira_piloto': "/static/img/pilotos/" + random.choice(bandeiras),
                'foto_piloto': "/static/img/pilotos/" + random.choice(fotos),
                'num_carro': carro['num'],
                'nome_equipe': equipe['nome'],
                'logo_equipe': "/static/img/equipes/" + random.choice(logos)
            }
        return dados