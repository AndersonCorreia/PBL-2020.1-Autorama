# coding=utf-8
from models.Qualificatoria import Qualificatoria
from threading import Thread

class QualificatoriaThread(Thread):

	def __init__ (self, corrida_id = None):
		Thread.__init__(self)
		self.qualificatoria = Qualificatoria(corrida_id)
		self.corrida = self.qualificatoria #para compatibilidade com a thread de interromper corrida
  
	def run(self):
		self.qualificatoria.qualificatoria()
		self.qualificatoria.qualificatoriaAcompanhar()