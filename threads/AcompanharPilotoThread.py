# coding=utf-8
from models.usuario.Autorama import Autorama as AutoramaUser
from threading import Thread

class AcompanharPilotoThread(Thread):

	def __init__ (self, tag):
		Thread.__init__(self)
		self.autorama = AutoramaUser() 
		self.tag = tag
  
	def run(self):
		self.autorama.getDataPilotMqtt(self.tag)