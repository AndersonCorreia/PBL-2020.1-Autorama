#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
from models.Autorama import Autorama

autorama = Autorama()

reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=115200)
reader.set_region("NA2")
reader.set_read_plan([1], "GEN2", read_power=1100)


def read():
    print(reader.get_model())
    print(reader.get_supported_regions())
    tags = reader.read(1000)
    if len(tags):
        tag = {"EPC": {"tag": tags[0].epc.decode("utf-8") , "timestamp": tags[0].epc.decode("utf-8")} , 'success': True }
        autorama.setLastTag(tag)
        return tag
    
    return {"EPC": {"tag": '', "timestamp": ''}, 'success': False }

def readAll():
    tags = reader.read()
    if len(tags):
        autorama.setLastTag(tags[-1])
        return tags

    return "Nenhuma tag foi lida"