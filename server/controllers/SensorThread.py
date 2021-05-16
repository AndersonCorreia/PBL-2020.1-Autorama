# coding=utf-8
from server.models.Autorama import Autorama
from server.models.Leitor import Leitor
from server.mercury_.sensor import *
from threading import Thread

class SensorThread(Thread):

	def __init__ (self, pub, buffer, function='read_send'):
		Thread.__init__(self)
		self.pub = pub
		self.buffer = buffer
		self.funcao = function

	def run(self):
		if( self.funcao == 'read_send' or self.funcao == 'read'):
			try:
				if( self.funcao == 'read_send'):
					reader.start_reading(self.readAndSend)
				else:
					reader.start_reading(self.read)
		
				while(not self.buffer['close']):
					print("Buffer:")
					print(self.buffer)
					time.sleep(self.buffer['tempoMinimoVolta']/2)
			finally:
				saveLog(self.buffer)
				reader.stop_reading()
			return
		elif(self.funcao == 'send'):
			while(not self.buffer['close']):
				self.send()
				time.sleep(0.5)
			return
		elif(self.funcao == 'encerrar'):
			sub = self.pub.getSUB('/corrida/encerrar')
			sub.request()
			sub.requestRecv()# aguardar até receber mensagem no topico de encerrar corrida
			self.buffer['close'] = True
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
					self.pub.request(json.dumps(tag).encode('utf-8') )
					self.buffer['tagsSend'].append(tag)
					# print ("Tag não foi enviada com sucesso")
					# self.buffer['tagsNoSend'].insert(0,tag)
			except Exception as e: 
				print ("Other exception: %s" %str(e))
				print ("Tag não foi enviada com sucesso")
				self.buffer['tagsNoSend'].insert(0,tag)
    
	def read(self, tag):
		timestamp = float( tag.timestamp )
		epc = tag.epc.decode("utf-8")
		if(not self.buffer['close'] and self.buffer['tags'].count(epc) > 0 and (timestamp - float( self.buffer['ultimaLeitura'][epc] ) ) > self.buffer['tempoMinimoVolta'] ):# se passaram ao menos 10s registra a leitura
			print("tag lida:\n")
			print(tag)
			print("Tag valida, tempo desde a ultima leitura: ")
			print(timestamp - float( self.buffer['ultimaLeitura'][epc] ) )
			# TagsNoSend é uma fila FIFO
			self.buffer['tagsNoSend'].append({"tag": epc , "timestamp": timestamp, "time": timestamp - float(self.buffer['timestamp_inicial']) } )
			self.buffer['ultimaLeitura'][epc] = timestamp
    
	def send(self):
		try: 
			while( len(self.buffer['tagsNoSend']) > 0 and not self.buffer['close']):
				tag = self.buffer['tagsNoSend'].pop(0)#sempre pega a primeira na fila para enviar
				print("Enviando a tag:\n")
				print(tag)
				print('\n')
				self.pub.request(json.dumps(tag).encode('utf-8') )
				self.buffer['tagsSend'].append(tag)
				# print ("Tag não foi enviada com sucesso")
				# self.buffer['tagsNoSend'].insert(0,tag)
		except Exception as e: 
			print ("Exception: %s" %str(e))
			print ("Tag não foi enviada com sucesso")
			self.buffer['tagsNoSend'].insert(0,tag)
     