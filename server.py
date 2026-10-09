import socket
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

def continuethread(num, client, address):
    print("Connection number: ", num)

    try:
        print("Connection from: ", address)
        data = client.recv(1024)
        if not data: 
            print("Connection closed")
            return
        times = int(data.decode())
        print("Incoming number of messages: ", times)
        client.sendall(b"Acknowledged")
        while (times):
            data = client.recv(1024)
            if not data:
                print("Connection closed")
                return
            data = data.decode()
            time.sleep(2)
            print("Connection number: ", num, " Data: ", data)

            client.sendall(b"Thanks, received\n")
            times -= 1
    except ConnectionResetError:
        print("Connection reset error")
    finally:
        print("Closing socket number: ", num)
        client.close()

print("server started")
count = 0
while True:
    client, address = server.accept()
    threading.Thread(
        target=continuethread,
        args = (count, client, address)
    ).start()
    count += 1
    

    