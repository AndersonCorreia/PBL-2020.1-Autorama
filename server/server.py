# coding=utf-8
import socket 
import sys
import argparse
import json
from ServerThread import ServerThread
from mqtt.SUB import Subscriber
from mqtt.PUB import Publisher

parser = argparse.ArgumentParser(description='arg')
parser.add_argument('--host', '-ip',help= "host/ip para conexão", default='node02.myqtthub.com')
parser.add_argument('--port', '-p', type=int, help= "porta usada para a conexão", default=1883)
parser.add_argument('--mqttid', '-mid', help= "mqtt: Id do dispositivo", default='1')
parser.add_argument('--mqttuser', '-mu', help= "mqtt: usuario", default='cliente1')
parser.add_argument('--mqttpassword', '-mp', help= "mqtt: senha", default='24680')
args = parser.parse_args()

def server(host = args.host, port = args.port, id = args.mqttid, user = args.mqttuser, password = args.mqttpassword):
    sub = Subscriber(host, port, id, user, password)
    sub.request()
    while True: 
        msg = sub.requestRecv(False)
        print(msg)
        data = msg.payload
        data["path"] = msg.topic
        pub = Publisher(host, port, id, user, password, msg.topic + '/response')
        serverT = ServerThread(data, pub)
        serverT.start()  
server()