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
    tags = reader.read()
    epcs = list(map(lambda tag: tag, reader.read()))
    print(tags)
    print(type(epcs))
    if len(tags):
#       autorama.setLastTag(tags[0])
        return epcs[0]
    
    return "Nenhuma tag foi lida"

def readAll():
    tags = reader.read()
    print(tags)
    if len(tags):
        autorama.setLastTag(tags[-1])
        return tags

    return "Nenhuma tag foi lida"