# coding=utf-8
from models.usuario.Autorama import Autorama as AutoramaUser
from threading import Thread

class AcompanharPilotoThread(Thread):

	def __init__ (self, id):
		Thread.__init__(self)
		self.autorama = AutoramaUser() 
		self.piloto_id = id
  
	def run(self):
		self.autorama.getDataPilotMqtt(self.piloto_id)