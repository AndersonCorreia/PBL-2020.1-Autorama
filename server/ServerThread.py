# coding=utf-8
from server.mqtt import PUB
from server.controllers.AutoramaController import AutoramaController
import json
from server.models import Botão
from threading import Thread

class ServerThread(Thread):
    
    def __init__(self, data, pub):
        Thread.__init__(self)
        self.data = data
        self.pub = pub

    def run(self):
        if self.data:
            response = self.route(self.data, self.pub)
            self.pub.request(self.data['path'],response.encode('utf-8'))
            
    def route(self, data, pub):
        print("data\n")
        print(data)
        if data['path']:
            dados = self.redirecionamento(pub, data['path'], data['headers'])
            print("dados\n")
            print(dados)
            return json.dumps({'success': dados['success'], "response": dados['dados']})
        else:
            return json.dumps({'success': False, "response": {"erro": "O topico não foi informado"} })

    def redirecionamento(self,pub, path, headers=[]):
        if path == "/test":
            return {"success": True, 'dados': ''}

        if path == "/config/leitor":
            AutoramaController.setConfigLeitor(headers)
            return {'success': True, 'dados': ''}

        if path == "/configuração/carro":
            return AutoramaController.readTag()

        if path == "/autorama/tags/read":
            return AutoramaController.readTag()
        
        if path == "/corrida/qualificatoria/carros":
            return AutoramaController.definirTagsParaLeitura(headers)
        
        if path == "/corrida/qualificatoria/acompanhar":
            return AutoramaController.qualificatoria(headers, pub)
    
        if path == "/button":
            Botão.button()
            return {'success': True, 'dados': ''}

        return {'success': False, 'dados': 'Rota não encontrada'}