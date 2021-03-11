# coding=utf-8
# from server.instance import server
# from controlers.readData import *
from socket_.Client import Client
import sys
import argparse

param = sys.argv[1:]
parser = argparse.ArgumentParser(description='arg')
parser.add_argument('--host', '-ip', help= "host/ip para conexão", default='172.16.1.0')
parser.add_argument('--port', '-p', type=int, help= "porta usada para a conexão", default=2021)
parser.add_argument('--data_payload', '-dp', type=int, help= "A quantidade maxima de dados recebidos de uma vez",
                    default='2048')
args = parser.parse_args()

Connection = Client(args.host, args.port, args.data_payload)

Connection.request()#rota padrão devolve todos os dados do arquivo autorama.json
Connection.request("/autorama/tags/read")#requisitando a leitura de uma tag
Connection.request("/autorama/tags/last")#pegando ultima tag lida

#server.run()