import socket
import threading
import time
import uuid

PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())

ADDRESS = (HOST,PORT)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HEADER = 64

server.bind(ADDRESS)
message_handler = {}
client_list = []


def handle_client(conn, adds, id):
    print(conn)
    print(adds)
    # global message_handler
    # message_handler[id] = 
    global client_list
    connected = True
    while connected:
        mesg_length = conn.recv(HEADER).decode('utf-8')
        if mesg_length:
            mesg = conn.recv(int(mesg_length)).decode('utf-8')
            if mesg == 'exit':
                connected = False
            print(mesg)
            msg_len = len(mesg)
            mesg_len = f"{msg_len}{' '*(HEADER - len(str(msg_len)))}"
            conn.sendall(mesg_len.encode('utf-8'))
            conn.sendall(mesg.encode('utf-8'))
            
    print(f"Server {adds} Disconnected!")
    conn.close()

    time.sleep(10)

def start():
    server.listen()
    while True:
        conn, adds = server.accept()
        id = uuid.uuid4().hex
        conn.send(str(adds).encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(conn,adds,id))
        thread.start()
        client_list.append({id:adds})
        print(f"[Active Connection] {adds}   {threading.active_count() - 1}")

print("Starting The SERVER..")
print(f"Server Started on {HOST}:{PORT}")
start()



