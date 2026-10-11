# Project Progress

## Day 1

### Update 1
- Implemented a TCP echo chamber with a client and server.
- The client informs the server about the number of incoming messages.
- The server accepts the specified number of messages and then disconnects.
- No message error tolerance has been implemented yet.

### Update 2
- Implemented threading so the server can handle multiple connections concurrently.
- Added error handling to gracefully close connections when a socket closes unexpectedly.
- Added a forced timeout check to test concurrency behavior.

## Day 2

### Update 1
-Implemented a message sharing and accepting protocol for both client and server where the client first sends a header containing the exact message length of the payload

## Day 3

### Update 1
-Implemented 3 different client types, c1 sends whole message at once, c2 sends message 1 byte at a time, c3 sends 3 messages at once
-let server handle any type of message

### Update 2

-Implemented a client which sends JSON requests in form of bytes and gets server response accordingly
-Server now handles decoding the json request and encoding the json response
-The requests handled are PING, ECHO, QUIT, invalid requests and non json requests

  
