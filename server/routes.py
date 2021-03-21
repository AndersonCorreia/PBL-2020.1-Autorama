# coding=utf-8
from controllers.AutoramaController import AutoramaController
import json

def route(data):
    data = json.loads(data)
    if data['path'] and data['method']:
        dados = redirecionamento(data['path'], data['method'], data['headers'])
        return json.dumps({'success': True, "response": dados})
    else:
        return json.dumps({'success': False, "response": {"erro": "O path e/ou method não foram informados"} })

def redirecionamento(path, method, headers=[]):
    if path == "/config/leitor":
        if method == "POST":
            AutoramaController.setConfigLeitor(headers)
            return {'success': True}

    if path == "/autorama/tags/read":
        if method == "GET":
            return AutoramaController.readTag()

    if path == "/autorama/tags/last":
        if method == "GET":
            return AutoramaController.getLastTag()
