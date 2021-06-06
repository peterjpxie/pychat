#!/usr/bin/env python3
# Orig: https://gist.github.com/schedutron/cd925247bfc4f8ae7930bbd99984a441
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging

logging.basicConfig(filename='serv.log',level=logging.DEBUG,format='%(asctime)s %(message)s', filemode='w',datefmt='%Y-%m-%d %I:%M:%S')
log = logging.getLogger('')

clients = {}
addresses = {}

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    global clients, addresses
    while True:
        client, client_address = SERVER.accept()
        log.info("%s:%s has connected." % client_address)
        print("%s:%s has connected." % client_address)
        # client.send(bytes("Type your name and send to start chat.", "utf8"))
        addresses[client] = client_address
        # Thread(target=handle_client, args=(client,)).start()
        Thread(target=handle_client, args=[client]).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    global clients, addresses
    # Modify client to send name on connection
    client.send(bytes("Type your name and click send to start chat.", "utf8"))
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! Type to chat now.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    
    receive_except = False
    send_except = False
    def close_client(log_msg):
        print(log_msg )
        log.info(log_msg )
        client.close()
        del clients[client]
        broadcast(bytes("%s has left the chat." % name, "utf8"))
        
    while True:
        try:
            msg = client.recv(BUFSIZ)
        # except ConnectionResetError:
        except:
            close_client('Receive exception detected on client. It is likely client has disconnected. Closing socket connection.')
            break

        if not msg: # maybe not necessary
            close_client('Empty message received on client. Closing socket connection.')
            break
            
        if msg != bytes("{quit}", "utf8"): # Receive quit on client windows close
            broadcast(msg, name+": ")
        else:
            # client.send(bytes("{quit}", "utf8"))
            close_client('Received quit from client. Closing socket connection.')
            break
            
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    global clients, addresses
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
       
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    log.info("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
