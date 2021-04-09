# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
from mercury_.sensor import *
from threading import Thread

class SensorThread(Thread):

	def __init__ (self, client, buffer, function='misto'):
		Thread.__init__(self)
		self.client = client
		self.buffer = buffer
		self.funcao = 'misto'

	def run(self):
		if( self.funcao == 'misto'):
			self.misto()
   
	def misto(self):
		reader.start_reading(self.readingMisto)
		#depois fazer condição de parada que tambem fecha a conexão
		time.sleep(10)
		reader.stop_reading()
		
	def readingMisto(self, tag):
		print(tag)
		timestamp = float( tag.timestamp )
		epc = tag.epc.decode("utf-8")
		if(self.buffer['tags'].count(epc) > 0 and (timestamp - float( self.buffer['ultimaLeitura'][epc] ) ) > 10 ):# se passaram ao menos 10s registra a leitura
			# TagsNoSend é uma fila FIFO
			self.buffer['tagsNoSend'].append({"tag": epc , "timestamp": timestamp, "time": timestamp - float(self.buffer['timestamp_inicial']) } )
			try: 
				while( len(self.buffer['tagsNoSend']) > 0 ):
					tag = self.buffer['tagsNoSend'].pop(0)#sempre pega a primeira na fila para enviar
					print(tag)
					print('\n')
					self.client.send(json.dumps(tag).encode('utf-8') )
					data = self.client.recv(data_payload)
					if( data['success'] == True):#cliente deve retornar que recebeu a informação com successo
						self.buffer['tagsSend'].append(tag)
						if( data['encerrarCorrida'] == True):
							self.client.close()
							#encerrar a thread nesse caso
					else:
						self.buffer['tagsNoSend'].insert(0,tag)
			except Exception as e: 
				print ("Other exception: %s" %str(e))
				print ("Tag não foi enviada com sucesso")
				self.buffer['tagsNoSend'].insert(0,tag)
     