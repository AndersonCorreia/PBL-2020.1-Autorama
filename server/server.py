# coding=utf-8
import socket 
import sys
import argparse
from routes import *

parser = argparse.ArgumentParser(description='arg')
parser.add_argument('--host', '-ip',help= "host/ip para conexão", default='172.16.1.0')
parser.add_argument('--port', '-p', type=int, help= "porta usada para a conexão", default=5030)
parser.add_argument('--data_payload', '-dp', type=int,help= "A quantidade maxima de dados recebidos de uma vez",
                    default='2048')
parser.add_argument('--listen_qtd', '-l', type=int,help= "Numero maximo de conexões ativas.",
                    default='204')
args = parser.parse_args()

def server(host = args.host, port = args.port, listen = args.listen_qtd):
    data_payload = args.data_payload #The maximum amount of data to be received at once
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    # Enable reuse address/port 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    print ("Starting server on %s port %s" % server_address)
    sock.bind(server_address)
    # Listen to clients, argument specifies the max no. of queued connections
    sock.listen(listen) 
    i = 0
    while True: 
        client, address = sock.accept() 
        data = client.recv(data_payload)
        data = json.loads(data)
        if data:
            response = route(data, client)
            client.send(response.encode('utf-8'))
        # end connection
        if not data['remainsOpen']:
            client.close()       
server()