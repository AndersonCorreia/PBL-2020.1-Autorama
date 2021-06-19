# coding=utf-8
from mqtt import PUB
from controllers.AutoramaController import AutoramaController
import json
# from models import Botão
from threading import Thread

class ServerThread(Thread):
    
    def __init__(self, data, sub):
        Thread.__init__(self)
        print('data')
        print(data)
        self.data = data
        self.sub = sub

    def run(self):
        if self.data:
            response = self.route(self.data, self.sub)
            self.sub.publishResponse(self.data['path'],response)
            
    def route(self, data, sub):
        print("data\n")
        print(data)
        if data['path']:
            dados = self.redirecionamento(sub, data['path'], data['headers'])
            print("dados\n")
            print(dados)
            return {'success': dados['success'], "response": dados['dados']}
        else:
            return {'success': False, "response": {"erro": "O topico não foi informado"} }

    def redirecionamento(self,sub, path, headers=[]):
        if path == "/test":
            return {"success": True, 'dados': ''}

        if path == "/config/leitor":
            AutoramaController.setConfigLeitor(headers)
            return {'success': True, 'dados': ''}

        if path == "/config/carro":
            #return AutoramaController.readTag()
            return AutoramaController.readTagSimulate() 

        if path == "/autorama/tags/read":
            return AutoramaController.readTag()
        
        if path == "/corrida/carros":
            return AutoramaController.definirTagsParaLeitura(headers)
        
        if path == "/corrida/acompanhar":
            return AutoramaController.corrida(headers, sub)
    
        if path == "/button":
            # Botão.button()
            return {'success': True, 'dados': ''}

        return {'success': False, 'dados': 'Rota não encontrada'}
