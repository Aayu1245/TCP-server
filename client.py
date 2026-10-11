import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_message(client, message):
    byte_message = message.encode("utf-8")
    header = struct.pack("!I", len(byte_message))
    final_message = header + byte_message   
    try:
        client.sendall(final_message)
        print("sent message")
        resp = client.recv(1024).decode()
        return 1, resp
    except Exception as e:
        return -1, str(e)



client.connect(("127.0.0.1", 5000))


mess = "Message No. 0"
code, resp = send_message(client, mess)
print(code, ", ", resp)



print("Messages sent, closing now")
client.close()
