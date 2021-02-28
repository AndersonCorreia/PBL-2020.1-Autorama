import socket
import sys
import argparse

param = sys.argv[1:]
parser = argparse.ArgumentParser(description='arg')
parser.add_argument('--host', '-ip', help= "host/ip para conexão", default='localhost')
parser.add_argument('--port', '-p', type=int, help= "porta usada para a conexão", default=8082)
parser.add_argument('--data_payload', '-dp', help= "A quantidade maxima de dados recebidos de uma vez",
                    default='2048')
args = parser.parse_args()

def client(host = args.host, port = args.port): 
    # Create a TCP/IP socket 
    # Connect the socket to the server 
    server_address = (host, port) 
    print ("Connecting to %s port %s" % server_address) 
    # Send data 
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect(server_address) 
        try: 
            # Send data 
            message = input("Escreva a mensagem para ser enviada:\n")
            print ("Sending %s" % message) 
            sock.sendall(message.encode('utf-8')) 
            # Look for the response  
            data = sock.recv(args.data_payload)
            print ("Received: %s" % data) 
        except socket.error as e: 
            print ("Socket error: %s" %str(e)) 
        except Exception as e: 
            print ("Other exception: %s" %str(e)) 
        finally: 
            print ("Closing connection to the server") 
            sock.close()
client()
