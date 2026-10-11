import socket
import struct
import time
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_message(client, m1, m2, m3):
    byte_message1 = m1.encode("utf-8")
    byte_message2 = m2.encode("utf-8")
    byte_message3 = m3.encode("utf-8")
    header1 = struct.pack("!I", len(byte_message1))
    header2 = struct.pack("!I", len(byte_message2))
    header3 = struct.pack("!I", len(byte_message3))
    final_message1 = header1 + byte_message1
    final_message2 = header2 + byte_message2
    final_message3 = header3 + byte_message3  
    try:
        client.sendall(final_message1 + final_message2 + final_message3)
        print("sent message")
        time.sleep(7)
        resp = client.recv(1024)

        print(resp.decode())
        return 1, resp
    except Exception as e:
        return -1, str(e)


client.connect(("127.0.0.1", 5000))


mess1 = "Hihi"
mess2 = "Goat"
mess3 = "Messi"
code, resp = send_message(client, mess1, mess2, mess3)
print(code, ", ", resp)



print("Messages sent, closing now")
client.close()