#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
from models.Autorama import Autorama

autorama = Autorama()
Client = None
log = None
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

def loadLog():
    log = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/leitor.json", 'r').read() )
    return log
  
def saveLog():
    dados = json.dumps(log, indent=4, ensure_ascii=False, skipkeys=False)
    open(os.path.dirname(os.path.realpath(__file__))+"/leitor.json", 'w').write(dados)
  
def setTagsForRead(tags):
    loadLog()
    log['tags'] = tags
    saveLog()
    