#!/usr/bin/env python3
from __future__ import print_function
import time
from datetime import datetime
import mercury
from models.Autorama import Autorama

reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=115200)
autorama = Autorama()

print(reader.get_model())
print(reader.get_supported_regions())

reader.set_region("EU3")
reader.set_read_plan([1], "GEN2", read_power=1100)

def read():
    tags = reader.read(2000)
    print(tags)
    if len(tags):
        autorama.setLastTag(tags[0])
        return tags[0]
    
    return "Nenhuma tag foi lida"

def readAll():
    tags = reader.read(2000)
    print(tags)
    if len(tags):
        autorama.setLastTag(tags[-1])
        return tags

    return "Nenhuma tag foi lida"