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
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish      
        mqtt.Client.connected_flag=False

    def request(self, message="", path= None):
        if path != None:
            self.topic = path
        self.client.connect(self.host, self.port)

        self.client.loop_start()
        while not self.client.connected_flag:
            time.sleep(1)

        # Send data 
        message = json.dumps({"headers": message})
        ret = self.client.publish(self.topic, message.encode('utf-8'), 0)   #using qoS-0 
        logging.info("published return="+str(ret))
        
        self.client.loop_stop()
        self.client.disconnect()

    #create functions for callback
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

    def reset(self):
        ret = self.client.publish("/test", "", 0, True)
        
    def setTopic(self, topic):
        self.topic = topic
    
    def getSUB(self, topic = None):
        return Subscriber(self.host, self.port, self.ID, self.user, self.passwd, topic)
# para teste
# pub = Publisher("node02.myqtthub.com", 1883, "2", "cliente2", "135790")
# pub.request("/test", "teste")