import socket
import struct
import time
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_message(client, m1, m2, m3, m4):
    byte_message1 = m1.encode("utf-8")
    byte_message2 = m2.encode("utf-8")
    byte_message3 = m3.encode("utf-8")
    byte_message4 = m4.encode("utf-8")
    header1 = struct.pack("!I", len(byte_message1))
    header2 = struct.pack("!I", len(byte_message2))
    header3 = struct.pack("!I", len(byte_message3))
    header4 = struct.pack("!I", len(byte_message4))
    final_message1 = header1 + byte_message1
    final_message2 = header2 + byte_message2
    final_message3 = header3 + byte_message3  
    final_message4 = header4 + byte_message4
    try:
        client.sendall(final_message1 + final_message2 + final_message3 + final_message4)
        print("sent message")
        resparr = []
        for i in range(4):
            code, resp = recv(client)
            if not resp:
                break
            resparr.append(resp)

        return 1, resparr
    except Exception as e:
        return -1, str(e)

def recv(client):
    data = client.recv(4)
    if not data:
        return -2, ""
    data = struct.unpack("!I", data)[0]
    code, message = recv_exactly(client, data)
    message = message.decode("utf-8")
    return code, message
def recv_exactly(client, data):
    message = bytearray()
    try:
        while(len(message) < data):
            cur_message = client.recv(data-len(message))
            if not cur_message:
                return 0, message
            message.extend(cur_message)
        return 1, message
    except (OSError, UnicodeDecodeError) as e:
        return -1, str(e)

client.connect(("127.0.0.1", 5000))

def ping(id):
    return json.dumps({"id": id, "type": "PING", "data": {}})

def echo(id, data):
    return json.dumps({"id": id, "type": "ECHO", "data": data})

def quiter(id):
    return json.dumps({"id": id, "type": "QUIT", "data": {}})

def invalid(id):
    return json.dumps({"type": "INVALID", "data":{}})

mess1 = ping(1)
mess2 = echo(2, "yoo")
mess3 = quiter(3)
mess4 = invalid(4)

code, resp = send_message(client, mess1, mess2, mess3, mess4)
for x in resp:
    print(f'{x}\n')



print("Messages sent, closing now")
client.close()
