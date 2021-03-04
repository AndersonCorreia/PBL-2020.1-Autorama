# coding=utf-8
import socket

def client(host='25.11.202.228', port=5555): 
    # Connect the socket to the server 
    server_address = (host, port) 
    print ("Connecting to %s port %s" % server_address) 
    data_payload = 2048

    while(True):
        # Create a TCP/IP socket 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect(server_address) 
        # Send data
        try:  
            message = input("Your message: ")
            print ("Sending %s" % message) 
            sock.sendall(message.encode('utf-8')) 
            # Look for the response  
            data = sock.recv(data_payload)
            print ("Received: %s" % data) 
        
        except socket.error as e: 
            print ("Socket error: %s" %str(e))
        except Exception as e: 
            print ("Other exception: %s" %str(e))
        finally:
            sock.close()

client()
