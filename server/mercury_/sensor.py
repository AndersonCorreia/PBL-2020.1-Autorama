#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
from models.Autorama import Autorama
import json
import os
from models.Leitor import Leitor

leitor = Leitor()
autorama = Autorama()
config = leitor.getDados()
reader = mercury.Reader(config['serial'], int(config['baudrate']))
reader.set_region(config['region'])
reader.set_read_plan([int(config['antena'])], config['protocol'], read_power=int(config['read_power']))


def read():
    print(reader.get_model())
    print(reader.get_supported_regions())
    tags = reader.read(2000)
    print(tags)
    if len(tags):
        tagsData = []
        for tag in tags:
            tagsData.append({"tag": tag.epc.decode("utf-8") , "timestamp": tag.timestamp})
        data = {"dados": tagsData , 'success': True }
        return data
    
    return {"dados": {"tag": '', "timestamp": ''}, 'success': False }

def loadLog():
    log = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/logleitura.json", 'r').read() )
    return log
  
def saveLog(log):
    dados = json.dumps(log, indent=4, ensure_ascii=False, skipkeys=False)
    open(os.path.dirname(os.path.realpath(__file__))+"/logleitura.json", 'w').write(dados)
  
def setTagsForRead(tags, tempoMinimoVolta):
    log = loadLog()
    log['tags'] = tags
    log['tempoMinimoVolta'] = tempoMinimoVolta
    log['close'] = False
    log['timestamp_inicial'] = time.time()
    log['tagsSend'] = []
    log['tagsNoSend'] = []

    ultimaLeitura = {}
    for tag in tags:
        ultimaLeitura[tag] = time.time()
    log['ultimaLeitura'] = ultimaLeitura
    
    print('salvou estas tags, para leitura')
    print(log)
    saveLog(log)
    
def setLogTimestampInicial():
    log = loadLog()
    log['timestamp_inicial'] = time.time() + 5.5 #5.5 segundos para compensar a contagem regressiva
    saveLog(log)