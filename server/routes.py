# coding=utf-8
from controllers.AutoramaController import AutoramaController

def response(data):
    data = json.loads(data)
    if data['path'] and data['method']:
        dados = redirecionamento(data['path'], data['method'], data['headers'])
        return json.dumps({'success': True, "response": dados})
    else:
        return json.dumps({'success': False, "response": {"erro": "O path e/ou method não foram informados"} })

def redirecionamento( path, method, headers=[]):
    if data['path'] == "autorama/all":
            if data['method'] == "GET":
                return AutoramaController.getAll()
            
    if data['path'] == "autorama/tags/last":
        if data['method'] == "GET":
                return AutoramaController.getLastTag()
