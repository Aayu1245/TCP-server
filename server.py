import socket
import threading
import time
import struct
import json
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()
server.settimeout(0.5)

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(threadName)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler("server.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)


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
    try:
        id = data["id"]
    except:
        data["id"] = random.randint(0,100)
    try:
        req = data["type"]
        dataa = data["data"]
    except:
        return error(data["id"])
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
    try:
        message = bytes(message.encode())
        client.sendall(message)
        logger.info("sent reply to client")
        return 1, ""
    except Exception as e:
        return -1, str(e)

def recv(client):
    data = bytearray()
    try:    
        try:
            while(len(data) < 4):
                chunk = client.recv(4-len(data))
                if not chunk:
                    return -2, ""
                data.extend(chunk)
        except (TimeoutError):
            return -5, "No client activity"
        if not data:
            return -2, ""
        data = struct.unpack("!I", data)[0]
        if (data > 1024*1024):
            return -3, "Msg too big"
        code, message = recv_exactly(client, data)
        try:
            message = message.decode("utf-8")
        except UnicodeDecodeError:
            message = message
        return code, message
    except OSError:
        return -6, ""

def recv_exactly(client, data):
    message = bytearray()
    try:
        while(len(message) < data):
            cur_message = client.recv(data-len(message))
            if not cur_message:
                return 0, message
            message.extend(cur_message)
        return 1, message
    except (UnicodeDecodeError) as e:
        return -1, str(e)
    except (TimeoutError) as t:
        return -5, "No client activity"
    except OSError:
        return -6, ""


def continuethread(num, client, address):
    logger.info(f"Connection number: {num}")

    try:
        logger.info(f"Connection from: {address}")
        while True:
            code, message = recv(client)
            if not message:
                break          
            if (code == 0):
                logger.warning(f"Connection closed in between, message: {message}")
            elif (code == -5):
                logger.warning(message)
                send_message(client, "No client activity, closing connection")
                break
            elif (code == -3):
                logger.warning(message)
                send_message(client, "Message too big")
                break
            else:
                logger.info(f"Msg received: {message}")
                if (code == 1):
                    reply = handle_request(message)
                    if (reply != ""):
                        send_message(client, reply)
                    else:
                        send_message(client, "Thanks, received. NO JSON")
                else:
                    send_message(client, "error")
        
    except ConnectionResetError:
        logger.error("Connection reset error")
    except OSError:
        logger.error(f"Program terminated")
    finally:
        logger.info(f"Closing socket number: {num}")
        client.close()


    
        
        
logger.info("server started")
count = 0
client = None

try:
    threads = []
    while True:
        try:
            client, address = server.accept()
        except TimeoutError:
            continue
        client.settimeout(30)
        t = threading.Thread(
            target=continuethread,
            args = (count, client, address)
        )
        t.start()
        threads.append(t)
        count += 1
except KeyboardInterrupt:
    logger.warning("Detected forced shutdown, closing server")
    for t in threads:
        t.join()
    if (client):
        client.close()
    server.close()




        
    

    