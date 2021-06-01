import socket
import threading
import uuid
import json
import time

"""
[FORMAT]

{
    'sid':'abcd',
    'rid':'efgh',
    'option': 'send,disconnect,emit,init,exist',
    'status':'',
    'data':''
}

"""


PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST,PORT)
HEADER = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDRESS)


client_list = {}
pair_list = []



def send(msg,conn):
    msg_len = len(msg)
    send_msg_len = f"{msg_len}{' '*(HEADER - len(str(msg_len)))}"
    conn.send(send_msg_len.encode(FORMAT))
    conn.send(msg.encode(FORMAT))

def handle_clent(id):
    global client_list
    conn = client_list.get(id).get('conn')
    adds = client_list.get(id).get('adds')
    connected = True
    init_data = {
        'option':'init',
        'data':id
    }
    init_data_str = json.dumps(init_data)
    send(init_data_str,conn)

    while connected:
        print(client_list)
        mesg_len = conn.recv(HEADER).decode(FORMAT)
        if mesg_len:
            try:
                mesg_len = int(mesg_len)
            except:
                print("HEADER ERROR")
                continue
            mesg = conn.recv(mesg_len).decode(FORMAT)
            mesg_dict = json.loads(mesg)
            sid = mesg_dict.get('sid')
            rid = mesg_dict.get('rid')
            if mesg_dict.get('option') == 'send':
                if rid in client_list.keys():
                    send(mesg,client_list.get(rid).get('conn'))
            elif mesg_dict.get('option') == 'disconnect':
                print("SERVER received the message 'disconnect'")
                if client_list.get(sid):
                    client_list.get(sid).get('conn').close()
                    del client_list[sid]
                    connected = False

            elif mesg_dict.get('option') == 'emit':
                for client_id in client_list.keys():
                    if client_id == mesg_dict.get('sid'):
                        continue
                    send(mesg,client_list.get(client_id).get('conn'))
                    # print(client_id)
            elif mesg_dict.get('option') == 'init':
                if mesg_dict.get('data') not in client_list:
                    client_list[mesg_dict.get('data')] = client_list.pop(id)
                    id = mesg_dict.get('data')
                else:
                    init_data['option'] = 'exist'
                    init_data_str = json.dumps(init_data)
                    send(init_data_str,conn)
        else:
            connected = False
    client_list.get(id).get('conn').close()
    del client_list[id]
    print(id)
    print("THREAD ENDED")
    

print("[SERVER] listening on %s:%s"%(HOST,PORT))
server.listen()

# def sync_client():
#     while True:
#         for client in client_list:
#             client.get('conn')
#         time.sleep(5)


# sync_thread = threading.Thread(target=)


while True:
    conn, adds = server.accept()
    id = uuid.uuid4().hex
    client_list[id] = {'conn':conn,'adds':adds}
    print(client_list)
    new_thread = threading.Thread(target=handle_clent, args=(id,))
    new_thread.start()

# class SocketServer:
#     def __init__(self,):









