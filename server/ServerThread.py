# coding=utf-8
from controllers.AutoramaController import AutoramaController
import json
from models import Botão
from threading import Thread

class ServerThread(Thread):
    
    def __init__(self, client, data):
        Thread.__init__(self)
        self.client = client
        self.data = data

    def run(self):
        if self.data:
            response = self.route(self.data, self.client)
            self.client.send(response.encode('utf-8'))
            # end connection
            if not self.data['remainsOpen']:
                self.client.close()
        else:
            self.client.close()
            
    def route(self, data, client):
        print("data\n")
        print(data)
        if data['path'] and data['method']:
            dados = self.redirecionamento(client, data['path'], data['method'], data['headers'])
            print("dados\n")
            print(dados)
            return json.dumps({'success': dados['success'], "response": dados['dados']})
        else:
            return json.dumps({'success': False, "response": {"erro": "O path e/ou method não foram informados"} })

    def redirecionamento(self, client, path, method, headers=[]):
        if path == "/test":
            if method == "GET":# posteriormente testa uma conexão real com o leitor
                return {"success": True, 'dados': ''}

        if path == "/config/leitor":
            if method == "POST":
                AutoramaController.setConfigLeitor(headers)
                return {'success': True, 'dados': ''}

        if path == "/configuração/carro":
            if method == "GET":
                return AutoramaController.readTag()

        if path == "/autorama/tags/read":
            if method == "GET":
                return AutoramaController.readTag()
            
        if path == "/corrida/qualificatoria/carros":
            if method == "POST":
                return AutoramaController.definirTagsParaLeitura(headers)
            
        if path == "/corrida/qualificatoria/acompanhar":
            if method == "GET":
                return AutoramaController.qualificatoria(headers, client)
        
        if path == "/button":
            if method == "GET":
                Botão.button()
                return {'success': True, 'dados': ''}

        return {'success': False, 'dados': 'Rota não encontrada'}