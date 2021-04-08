# coding=utf-8
from controllers.AutoramaController import AutoramaController
import json
from models import Botão

def route(data):
    data = json.loads(data)
    if data['path'] and data['method']:
        dados = redirecionamento(data['path'], data['method'], data['headers'])
        return json.dumps({'success': dados['success'], "response": dados['dados']})
    else:
        return json.dumps({'success': False, "response": {"erro": "O path e/ou method não foram informados"} })

def redirecionamento(path, method, headers=[]):
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
        
    if path == "/autorama/qualificatoria/init":
        if method == "POST":
            return AutoramaController.initQualificatoria(headers)
    
    if path == "/":
        if method == "GET":
            Botão.button()
            return {'success': True, 'dados': ''}