import json
import time
import paho.mqtt.client as mqtt
import logging
logging.basicConfig(level=logging.INFO)

class Subscriber:
    
    def __init__(self, host, port, ID, user, passwd, topic = "/#"):
        self.host = host
        self.port = port
        self.client = mqtt.Client(ID, True)
        self.client.username_pw_set(user, passwd)
        self.topic = topic
        self.receiveMsg = False
        self.msg = None
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def request(self, path=None):
        if path != None:
            self.topic = path
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    #create functions for callback
    def on_log(self, client, userdata, level, buf):
        logging.info(buf)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))
        client.subscribe(self.topic, 0) #qoS-0
        
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        logging.info(msg.topic+" "+msg.payload)
        msg.payload = json.loads(msg.payload)
        self.msg = msg
        self.receiveMsg = True
        
    def requestRecv(self, stop=True):
        while not self.receiveMsg:
            time.sleep(0.5)
        self.receiveMsg = False
        if stop :
            self.client.disconnect()
            self.client.loop_stop()
        return self.msg
        
    def setTopic(self, topic):
        self.topic = topic

# para teste
'''
sub = Subscriber("node02.myqtthub.com", 1883, "2", "cliente2", "135790")
sub.request("/config/carro")
print(sub.requestRecv(False))
'''