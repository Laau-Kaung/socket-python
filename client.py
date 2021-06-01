import socket
import threading
import json
import keyboard


PORT = 5050
HOST = '13.212.164.38'
ADDRESS = (HOST,PORT)
HEADER = 64
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)
my_id = str(input('Enter your ID : '))
my_rid = str(input('Enter your partner ID : '))
continue_listen = True

def send_str(msg,option,rid=False,type='string'):
    global my_id
    global continue_listen
    try:
        data_format = {
            'sid':my_id,
            'rid':rid,
            'option':option,
            'status':200,
            'type':type,
            'data':msg
        }
        data_format = json.dumps(data_format)
        msg_len = len(data_format)
        send_msg_len = f"{msg_len}{' '*(HEADER - len(str(msg_len)))}"
        client.send(send_msg_len.encode(FORMAT))
        client.send(data_format.encode(FORMAT))
        if option == 'disconnect':
            continue_listen = False
    except:
        pass



def listen():
    global my_id
    global continue_listen
    while continue_listen:
        try:
            reply = client.recv(HEADER).decode(FORMAT)
            if reply:
                try:
                    reply_len = int(reply)
                except:
                    continue
                mesg = client.recv(reply_len).decode(FORMAT)
                mesg_dict = json.loads(mesg)
                if mesg_dict.get('option') == 'init':
                    if my_id !=mesg_dict.get('data'):
                        send_str(my_id,'init')
                    else:
                        my_id = mesg_dict.get('data')

                elif mesg_dict.get('option') == 'exist':
                    print("Your ID Already Exists and we used default ID")
                    my_id = mesg_dict.get('data')

                else:
                    print(f"{mesg_dict.get('sid')} send '{mesg_dict.get('data')}'")
        except:
            continue

listen_thread = threading.Thread(target=listen)
listen_thread.start()
input("Press Enter to continue")
while True:
    key_value = keyboard.read_event()
    msg = {
        'key':key_value.__dict__.get('name'),
        'event_type':key_value.__dict__.get('event_type')
    }
    if my_rid:
        if msg.get('key')=='a' or msg.get('key')=='s' or msg.get('key')=='d' or msg.get('key')=='w':
            send_str(msg,'send',rid=my_rid,type='key')








