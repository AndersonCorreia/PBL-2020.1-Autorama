# coding=utf-8
from models.Corrida import Corrida
from threading import Thread

class QualificatoriaThread(Thread):

	def __init__ (self, corrida_id = None):
		Thread.__init__(self)
		self.corrida = Corrida(corrida_id)
  
	def run(self):
        self.corrida.qualificatoria()
        self.corrida.qualificatoriaAcompanhar()