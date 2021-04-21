# coding=utf-8
from threading import Thread
from models.Leitor import Leitor

class InterromperCorridaThread(Thread):

	def __init__ (self, corrida):
		Thread.__init__(self)
		self.corrida = corrida
  
	def run(self):
		leitor = Leitor()
		result = leitor.getButton()
		if(result['success']):
			self.corrida.corridaEnd = True