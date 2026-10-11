import socket
import threading
import time
import struct
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()


def pong(id):
    return json.dumps({"id": id, "ok": True, "type": "PONG", "data": {}})
def echo(id, data):
    return json.dumps({"id": id, "ok": True, "type": "ECHO", "data": data})
def quiter(id):
    return json.dumps({"id": id, "ok": True, "type": "QUIT", "data": {}})
def error(id, message="unknown command"):
    return json.dumps({"id": id, "ok": False, "error": message})
router = {
    "PING": pong,
    "ECHO": echo,
    "QUIT": quiter
}

def handle_request(dump):
    try:
        data = json.loads(dump)
    except:
        return ""

    req = data["type"]
    if req in router:
        if req != "ECHO":
            func = router[req]
            stri = func(data["id"])
        else:
            func = router[req]
            stri = func(data["id"], data["data"])
    else:
        func = error
        stri = error(data["id"])
    return stri

def send_message(client, message):
    byte_message = message.encode("utf-8")
    header = struct.pack("!I", len(byte_message))
    final_message = header + byte_message   
    try:
        client.sendall(final_message)
        print("sent reply to client")
        return 1, ""
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

def continuethread(num, client, address):
    print("Connection number: ", num)

    try:
        print("Connection from: ", address)
        while True:
            code, message = recv(client)
            if not message:
                break          
            if (code == 0):
                print("Connection closed in between, message: ", message)
            else:
                print(message)
                if (code == 1):
                    reply = handle_request(message)
                    
                    if (reply):
                        send_message(client, reply)
                    else:
                        send_message(client, "Thanks, received. NO JSON")
                else:
                    send_message(client, "error")
        
    except ConnectionResetError:
        print("Connection reset error")
    finally:
        print("Closing socket number: ", num)
        client.close()

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
        
        
print("server started")
count = 0
while True:
    client, address = server.accept()
    threading.Thread(
        target=continuethread,
        args = (count, client, address)
    ).start()
    count += 1
    

    