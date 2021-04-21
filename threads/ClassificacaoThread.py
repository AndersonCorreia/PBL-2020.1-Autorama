# coding=utf-8
from models.Classificacao import Classificacao
from threading import Thread

class ClassificacaoThread(Thread):

	def __init__ (self, corrida_id = None):
		Thread.__init__(self)
		self.classificacao = Classificacao(corrida_id)
		self.corrida = self.classificacao #para compatibilidade com a thread de interromper corrida
  
	def run(self):
		self.classificacao.classificacao()
		self.classificacao.classificacaoAcompanhar()