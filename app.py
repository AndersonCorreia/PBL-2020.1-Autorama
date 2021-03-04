'''
from autorama import Autorama

autorama = Autorama()

print(autorama.dados)

autorama.save()
'''
from src.server.instance import server
from src.controlers.readData import *

server.run()