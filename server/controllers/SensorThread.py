# coding=utf-8
from models.Autorama import Autorama
from models.Leitor import Leitor
from mercury_.sensor import *
from threading import Thread

class SensorThread(Thread):

	def __init__ (self, client, buffer, function='read_send'):
		Thread.__init__(self)
		self.client = client
		self.buffer = buffer
		self.funcao = function

	def run(self):
		if( self.funcao == 'read_send' or self.funcao == 'read'):
			if( self.funcao == 'read_send'):
				reader.start_reading(self.readAndSend)
			else:
				reader.start_reading(self.read)
    
			while(not self.buffer['close']):
				time.sleep(self.buffer['tempoMinimoVolta'] + 1)
			reader.stop_reading()
		elif(self.funcao == 'send'):
			while(not self.buffer['close']):
				self.send()
				time.sleep(0.5)
		else:
			print("função deschonhecida para iniciar a thread do sensor: ")
			print(self.funcao)
			return
		
	def readAndSend(self, tag):
		timestamp = float( tag.timestamp )
		epc = tag.epc.decode("utf-8")
		print(tag)
		if(not self.buffer['close'] and self.buffer['tags'].count(epc) > 0 and (timestamp - float( self.buffer['ultimaLeitura'][epc] ) ) > self.buffer['tempoMinimoVolta'] ):# se passaram ao menos 10s registra a leitura
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
    
	def read(self, tag):
		timestamp = float( tag.timestamp )
		epc = tag.epc.decode("utf-8")
		print("tag lida:\n")
		print(tag)
		if(not self.buffer['close'] and self.buffer['tags'].count(epc) > 0 and (timestamp - float( self.buffer['ultimaLeitura'][epc] ) ) > self.buffer['tempoMinimoVolta'] ):# se passaram ao menos 10s registra a leitura
			print("Tag valida, tempo desde a ultima leitura: ")
			print(timestamp - float( self.buffer['ultimaLeitura'][epc] ) )
			# TagsNoSend é uma fila FIFO
			self.buffer['tagsNoSend'].append({"tag": epc , "timestamp": timestamp, "time": timestamp - float(self.buffer['timestamp_inicial']) } )
			self.buffer['ultimaLeitura'][epc] = timestamp
    
	def send(self, tag):
		try: 
			while( len(self.buffer['tagsNoSend']) > 0 ):
				tag = self.buffer['tagsNoSend'].pop(0)#sempre pega a primeira na fila para enviar
				print("Enviando a tag:\n")
				print(tag)
				print('\n')
				self.client.send(json.dumps(tag).encode('utf-8') )
				data = json.loads( self.client.recv(2048) )#se necessario lembra de pegar esse valor dos argumentos
				print("resposta do cliente: ")
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
			print ("Exception: %s" %str(e))
			print ("Tag não foi enviada com sucesso")
			self.buffer['tagsNoSend'].insert(0,tag)
     