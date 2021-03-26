# coding=utf-8
import socket
import json

class Client:
    
    def __init__(self, host, port, payload):
        self.host = host
        self.port = port
        self.payload = payload
    
    def request(self, path="/autorama/all", method="GET", headers={}):

        # Create a TCP/IP socket 
        # Connect the socket to the server 
        server_address = (self.host, self.port) 
        print ("Connecting to %s port %s" % server_address) 
        # Send data 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try:
            sock.connect(server_address) 
        except ConnectionRefusedError as error:
            raise RuntimeError('Conexão recusada') from error

        try: 
            # Send data 
            message = json.dumps({"path": path, "method": method, "headers": headers })
            print ("Sending %s" % message) 
            sock.sendall(message.encode('utf-8')) 
            # Look for the response  
            data = sock.recv(self.payload)
            print (data)
            return data
        except socket.error as e: 
            print ("Socket error: %s" %str(e)) 
        except Exception as e: 
            print ("Other exception: %s" %str(e)) 
        finally: 
            print ("Closing connection to the server") 
            sock.close()