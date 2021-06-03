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
        self.client.on_publish = self.on_publish
        mqtt.Client.connected_flag=False
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    def request(self, path=None):
        if path != None:
            self.topic = path
        while mqtt.Client.connected_flag == False:
            time.sleep(0.2)
        self.client.subscribe(self.topic, 0) #qoS-0

    #create functions for callback
    def on_log(self, client, userdata, level, buf):
        logging.info(buf)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))    
        mqtt.Client.connected_flag=True
        
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        logging.info("topico:" + msg.topic)
        logging.info("mensagem:" + msg.payload)
        msg.payload = json.loads(msg.payload)
        self.msg = msg
        self.receiveMsg = True
        
    def requestRecv(self, stop=True, topic=""):

        while not self.receiveMsg or ( topic != "" and topic != self.msg.topic):
            time.sleep(0.5)
        self.receiveMsg = False
        if stop :
            self.client.disconnect()
            self.client.loop_stop()
        return self.msg
        
    def setTopic(self, topic):
        self.topic = topic
    
    def on_publish(self, client,userdata,mid):            
        logging.info("data published \n")
        
    def publishResponse(self, path= None, message="", rt=False):
        if path != None:
            self.topic = path

        while not self.client.connected_flag:
            print('não conectado')
            time.sleep(1)
        # Send data 
        message = json.dumps({"headers": message})
        ret = self.client.publish(self.topic + '/response', message, 1, retain=rt)   #using qoS-0 
        logging.info("published return="+str(ret))
# para teste
# sub = Subscriber("node02.myqtthub.com", 1883, "marianalima0803@gmail.com", "marianasls", "oUJeeKGZ-RxhrHx4T")
# sub.request()
