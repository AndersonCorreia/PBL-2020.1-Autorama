import paho.mqtt.client as mqtt
import time
import logging
broker="node02.myqtthub.com"
port=1883
logging.basicConfig(level=logging.INFO)
#create functions for callback
def on_log(client, userdata, level, buf):
    logging.info(buf)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag=True
    else:
        logging.info("bad connection returned code="+str(rc))
        client.loop_stop()
def on_disconnect(client, userdata, rc):
    logging.info("client disconnected")
def on_publish(client,userdata,mid):            
    logging.info("data published \n")               
def reset():
    ret = cliente.publish("autorama/test", "", 0, True)  

mqtt.Client.connected_flag=False
cliente = mqtt.Client("2")                          
cliente.username_pw_set("cliente2", "135790")
cliente.on_log = on_log
cliente.on_connect = on_connect
cliente.on_disconnect = on_disconnect
cliente.on_publish = on_publish      

#establish connection
cliente.connect(broker,port)             
cliente.loop_start()
while not cliente.connected_flag:
    time.sleep(1)

time.sleep(3)
ret = cliente.publish("autorama/test", "teste 0", 0)   #using qoS-0 
print("published return="+str(ret))
time.sleep(3)
ret = cliente.publish("autorama/test", "teste 1", 1)    #using qoS-1
print("published return="+str(ret))
time.sleep(3)
ret = cliente.publish("autorama/test", "teste 2", 2)    #using qoS-2
print("published return="+str(ret))

time.sleep(5)
#reset()        # para apagar uma publicação que ficou salva com retain=True
cliente.loop_stop()
cliente.disconnect()