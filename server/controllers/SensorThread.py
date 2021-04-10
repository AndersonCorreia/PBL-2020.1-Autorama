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
		while(not self.buffer['close']):
			time.sleep(5)
		reader.stop_reading()
		
	def readingMisto(self, tag):
		timestamp = float( tag.timestamp )
		epc = tag.epc.decode("utf-8")
		if(not self.buffer['close'] and self.buffer['tags'].count(epc) > 0 and (timestamp - float( self.buffer['ultimaLeitura'][epc] ) ) > self.buffer['tempoMinimoVolta'] ):# se passaram ao menos 10s registra a leitura
			print(tag)
			print(timestamp - float( self.buffer['ultimaLeitura'][epc] ) )
			# TagsNoSend é uma fila FIFO
			self.buffer['tagsNoSend'].append({"tag": epc , "timestamp": timestamp, "time": timestamp - float(self.buffer['timestamp_inicial']) } )
			self.buffer['ultimaLeitura'][epc] = timestamp
			try: 
				while( len(self.buffer['tagsNoSend']) > 0 ):
					tag = self.buffer['tagsNoSend'].pop(0)#sempre pega a primeira na fila para enviar
					print(tag)
					print('\n')
					self.client.send(json.dumps(tag).encode('utf-8') )
					data = json.loads( self.client.recv(2048) )#se necessario lembra de pegar esse valor dos argumentos
					print(data)
					if( data['success'] == True):#cliente deve retornar que recebeu a informação com successo
						print('tag enviada com sucesso')
						self.buffer['tagsSend'].append(tag)
						if( data['encerrarCorrida'] == True):
							self.client.close()
							self.buffer['close'] = True
							#encerrar a thread nesse caso
					else:
						print ("Tag não foi enviada com sucesso")
						self.buffer['tagsNoSend'].insert(0,tag)
			except Exception as e: 
				print ("Other exception: %s" %str(e))
				print ("Tag não foi enviada com sucesso")
				self.buffer['tagsNoSend'].insert(0,tag)
     