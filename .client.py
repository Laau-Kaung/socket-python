import socket
import threading
import time

PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
HEADER = 64

ADDRESS = (HOST,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


client.connect(ADDRESS)

my_id = client.recv(HEADER).decode('utf-8')
def send(msg):
    msg_len = len(msg)
    msg_len = f"{msg_len}{' '*(HEADER - len(str(msg_len)))}"
    client.send(msg_len.encode('utf-8'))
    msg = str(msg).encode('utf-8')
    client.send(msg)
    # disconnect_msg = 'Disconnect!!!!!!!!!!100'
    # server.send(disconnect_msg.encode('utf-8'))

def disconnect():
    msg = 'Disconnect!!!!!!!!!!100'
    msg_len = len(msg)
    client.send(str(msg_len).encode('utf-8'))
    client.send(msg.encode('utf-8'))

stop_thread = False

def listen():
    connected = True
    
    while connected:
        global stop_thread
        if stop_thread:
            break
        mesg_length = client.recv(HEADER).decode('utf-8')
        if mesg_length:
            mesg_length = int(mesg_length)
            mesg = client.recv(mesg_length).decode('utf-8')
            print(mesg)


thread = threading.Thread(target=listen)
thread.start()
while True:
    mymesg = str(input("Enter your message : "))
    send(mymesg)
    if mymesg == 'exit':
        break
stop_thread = True
thread.join()


