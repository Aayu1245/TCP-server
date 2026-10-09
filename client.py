import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(("127.0.0.1", 6000))
times = 6

while times:
    if (times == 6):
        print("Alerting server that 5 messages are coming")
        client.connect(("127.0.0.1", 5000))
        client.sendall(b"5")
        resp = client.recv(1024)
        print("Received: ", resp.decode())
        times -= 1
    client.sendall(b"Heyy")
    resp = client.recv(1024)
    print("Received: ", resp.decode())

    
    times -= 1

print("Messages sent, closing now")
client.close()
