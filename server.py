import socket
import threading
import time
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

def continuethread(num, client, address):
    print("Connection number: ", num)

    try:
        print("Connection from: ", address)
        while True:
            data = client.recv(4)
            if not data:
                break
            data = struct.unpack("!I", data)[0]
            code, message = recv_exactly(client, data)
            message = message.decode("utf-8")
            
            if (code == 0):
                print("Connection closed in between, message: ", message)
            else:
                print(message)
                if (code == 1):
                    client.sendall(b"Thanks, received")
                else:
                    client.sendall(b"error") 
        
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
    

    