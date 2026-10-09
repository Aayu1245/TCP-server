import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

print("server started")
while True:
    client, address = server.accept()
    print("Connection from: ", address)

    data = client.recv(1024)
    times = int(data.decode())
    print("Incoming number of messages: ", times)
    client.sendall(b"Acknowledged")
    while (times):
        data = client.recv(1024)
        data = data.decode()
        print(data)

        client.sendall(b"Thanks, received")
        times -= 1
    client.close()

    