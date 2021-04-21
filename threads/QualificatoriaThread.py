# coding=utf-8
from models.Qualificatoria import Qualificatoria
from threading import Thread

class QualificatoriaThread(Thread):

	def __init__ (self, corrida_id = None):
		Thread.__init__(self)
		self.qualificatoria = qualificatoria(corrida_id)
  
	def run(self):
		self.qualificatoria.qualificatoria()
		self.qualificatoria.qualificatoriaAcompanhar()