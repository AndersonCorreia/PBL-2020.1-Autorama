# coding=utf-8
from models.usuario.Autorama import Autorama as AutoramaUser
from threading import Thread

class CorridaUsuarioThread(Thread):

	def __init__ (self, classificacao):
		Thread.__init__(self)
		self.autorama = AutoramaUser()
		self.isClassificatoria = classificacao
  
	def run(self):
		self.autorama.getDadosCorridaMqtt(self.isClassificatoria)