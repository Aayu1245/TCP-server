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
  
