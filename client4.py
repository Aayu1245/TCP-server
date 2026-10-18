import socket
import struct
import time
import threading


def send_message(client, message):
    byte_message = message.encode("utf-8")
    header = struct.pack("!I", len(byte_message))
    final_message = header + byte_message   
    try:
        client.sendall(header)
        client.sendall(byte_message)
        resp = client.recv(1024).decode()
        print(resp)
        return 1, resp
    except Exception as e:
        return -1, str(e)


socks = []

try:
    for x in range(100):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 5000))
        socks.append(client)
        print(f"{x} connected")
        threading.Thread(target = send_message, args = (client, f"message no. {x}")).start()
except Exception as e:
    print(e)

