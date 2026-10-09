Day 1:
  Update 1:
    -Implemented a client and server tcp echo chamber where client alerts the server about the incoming number of messages, server accepts the given amount and            disconnects
    -No message error tolerance yet
  Update 2:
    -Implemented threading to let server handle multiple connections concurrently
    -added error handling to gracefully close connections in case of unexpected closing of socket
    -added forced timed wait to check concurrency 
  
