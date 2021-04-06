#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
from models.Autorama import Autorama

autorama = Autorama()
Client = null
reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=115200)
reader.set_region("NA2")
reader.set_read_plan([1], "GEN2", read_power=1100)


def read():
    print(reader.get_model())
    print(reader.get_supported_regions())
    tags = reader.read(1000)
    print(tags)
    if len(tags):
        tag = {"dados": {"tag": tags[0].epc.decode("utf-8") , "timestamp": tags[0].epc.decode("utf-8")} , 'success': True }
        autorama.setLastTag(tag)
        return tag
    
    return {"dados": {"tag": '', "timestamp": ''}, 'success': False }

def readAndSend(client):
    Client = client
    log = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/leitor.json", 'r').read() )
    reader.start_reading(reading)
    #depois fazer condição de parada que tambem fecha a conexão
    time.sleep(60)
    reader.stop_reading()
    
def reading(tag):
    print(tag)
    timestamp = int(tag.epc.decode("utf-8") )
    epc = tag.epc.decode("utf-8")
    if(log['tags'].count(epc) > 0 and (timestamp - int( log['ultimaLeitura'][epc] ) ) > 10 ):# se passaram ao menos 10s registra a leitura
        # TagsNoSend é uma fila FIFO
        log['tagsNoSend'].append({"tag": epc , "timestamp": timestamp, "time": timestamp - int(log['timestamp_inicial']) } )
        try: 
            while( len(log['tagsNoSend']) > 0 ):
                tag = log['tagsNoSend'].pop(0)#sempre pega a primeira na fila para enviar
                client.send(json.dumps(tag).encode('utf-8') )
                data = client.recv(data_payload)
                if( data['success'] == True):#cliente deve retornar que recebeu a informação com successo
                    log['tagsSend'].append(tag)
                else:
                    log['tagsNoSend'].insert(0,tag)
        except Exception as e: 
            print ("Other exception: %s" %str(e))
            print ("Tag não foi enviada com sucesso")
            log['tagsNoSend'].insert(0,tag)