#!/usr/bin/env python3
# orig: https://gist.github.com/schedutron/287324944d765ae0656eec6971ca40d8
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

# Parameters
client_name = ''

#----Now comes the sockets part----
# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)
HOST = '127.0.0.1'
PORT = 33000

global client_socket, msg_list, my_msg, top

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    try:
        client_socket.send(bytes(msg, "utf8"))
    # except ConnectionAbortedError:
    except:
        print ('Message send exception. Connect to server may be lost. Closing client...')
        client_socket.close()
        top.quit()
    if msg == "{quit}":
        print ('Client quits the chat. Closing client...')
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    # my_msg.set("{quit}")
    # send()
    try: client_socket.close()
    except: pass
    try: top.quit()
    except: pass



BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect(ADDR)
#except ConnectionRefusedError:
except:
    print('Cannot connect to server.')
    quit()

top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your name here")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg,width=50)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing) 

    
receive_thread = Thread(target=receive)
receive_thread.start()
# send client name on connection
# client_socket.send(bytes(client_name, "utf8")) 

tkinter.mainloop()  # Starts GUI execution.

