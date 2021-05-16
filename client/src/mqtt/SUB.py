import paho.mqtt.client as mqtt
import logging
logging.basicConfig(level=logging.INFO)

class Subscriber:
    
    def __init__(self, host, port, ID, user, passwd):
        self.host = host
        self.port = port
        self.client = mqtt.Client(ID, False)
        self.client.username_pw_set(user, passwd)
        self.topic = None
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def request(self, path="/#"):
        self.topic = path
        self.client.connect(self.host, self.port)
        self.client.loop_forever()

    #create functions for callback
    def on_log(self, client, userdata, level, buf):
        logging.info(buf)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))
        client.subscribe(self.topic, 0) #qoS-0
        
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logging.info(msg.topic+" "+msg.payload.decode("utf-8"))

# para teste
sub = Subscriber("node02.myqtthub.com", 1883, "marianalima0803@gmail.com", "marianasls", "oUJeeKGZ-RxhrHx4T")
sub.request()
