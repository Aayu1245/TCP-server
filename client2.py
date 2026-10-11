import socket
import struct
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_message(client, message):
    byte_message = message.encode("utf-8")
    byte_array = [byte_message[i:i+1] for i in range(len(byte_message))]
    header = struct.pack("!I", len(byte_message)) 
    try:
        client.sendall(header)
        for i in byte_array:
            time.sleep(1)
            client.sendall(i)
        print("sent message")
        resp = client.recv(1024).decode()
        return 1, resp
    except Exception as e:
        return -1, str(e)



client.connect(("127.0.0.1", 5000))



mess = "Message No. 1"
code, resp = send_message(client, mess)
print(code, ", ", resp)



print("Messages sent, closing now")
client.close()