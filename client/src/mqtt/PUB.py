from client.src.mqtt.SUB import Subscriber
import paho.mqtt.client as mqtt
import time
import logging
import json
logging.basicConfig(level=logging.INFO)

class Publisher:
    
    def __init__(self, host, port, ID, user, passwd, topic = "/"):
        self.host = host
        self.port = port
        self.ID = ID
        self.user = user
        self.passwd = passwd
        self.client = mqtt.Client(ID, False)
        self.client.username_pw_set(user, passwd)
        self.topic = topic
        self.receiveMsg = False
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish  
        self.client.on_message = self.on_message    
        mqtt.Client.connected_flag=False

    def request(self, path= None, message="", rt=False):
        if path != None:
            self.topic = path
        self.client.connect(self.host, self.port)

        self.client.loop_start()
        while not self.client.connected_flag:
            time.sleep(1)

        # Send data 
        message = json.dumps({"headers": message})
        ret = self.client.publish(self.topic, message, 0, retain=rt)   #using qoS-0 
        logging.info("published return="+str(ret))
        
        self.client.loop_stop()
        self.client.disconnect()
        
    def requestSub(self, path=None):
        if path != None:
            self.topic = path
        self.client.connect(self.host, self.port)
        self.client.loop_start()
        self.client.subscribe(self.topic, 0) #qoS-0

    # create functions for callback
    def on_log(self, client, userdata, level, buf):
        logging.info(buf)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag=True
        else:
            logging.info("bad connection returned code="+str(rc))
            client.loop_stop()

    def on_disconnect(self, client, userdata, rc):
        logging.info("client disconnected")

    def on_publish(self, client,userdata,mid):            
        logging.info("data published \n")
   
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        logging.info(msg.topic+" "+msg.payload)
        msg.payload = json.loads(msg.payload)
        self.msg = msg
        self.receiveMsg = True
        
    def reset(self):
        ret = self.client.publish(self.topic, "", 0, True)
        
    def setTopic(self, topic):
        self.topic = topic
    
    def getSUB(self, path = None):
        if path != None: topic = path
        else: topic = self.topic
        return Subscriber(self.host, self.port, self.ID, self.user, self.passwd, topic)
    
    # realizar um subscribe no mesmo topico que enviou informações e espera uma resposta
    # já devolve o payload da mensagem
    def requestRecv(self, stop=True):
        # sub = self.getSUB()
        self.requestSub()
        return self.requestRecvSub(stop).payload
    
    def requestRecvSub(self, stop=True):
        print('valor do stop ' + str(stop))
        while not self.receiveMsg:
            time.sleep(0.5)
        self.receiveMsg = False
        if stop :
            self.client.disconnect()
            self.client.loop_stop()
        return self.msg
# para teste
'''
pub = Publisher("node02.myqtthub.com", 1883, "1", "cliente1", "24680")
pub.request("/config/carro", "12345c")
'''