# C/C++ HTTP Server

### Contributors

- Ryan DeStefano

---

### Server File Tree

<pre>
c_server
\_ Makefile                    # Makefile for building all project artifacts
\_ README.md                   # README file for project documentation 
\_ bin
   \_ test.py                  # Python script for HTTP client
\_ include
   \_ server.h                 # C99 header file
\_ lib
   \_ mime.types               # File containing list of possible mimetypes
\_ src
   \_ forking.c                # C99 file for forking mode (multiple proceses)
   \_ handler.c                # C99 file for event handlers
   \_ request.c                # C99 file for HTTP requests
   \_ server.c                 # C99 file for main execution
   \_ single.c                 # C99 file for single mode (one process)
   \_ socket.c                 # C99 file for opening sockets to listen for HTTP requests
   \_ utils.c                  # C99 file for utility functions
\_ www
   \_ html
      \_ index.html            # Example HTML document
   \_ images
      \_ four_elements.jpg     # Example image file
      \_ math.jpg              # Example image file
      \_ minecraft.png         # Example image file
      \_ orion_nebula.jpg      # Example image file
   \_ scripts
      \_ env.sh                # Example CGI script (Shell)
      \_ gauss_elim            # Example C++ executable
      \_ hello.py              # Example CGI script (Python)
      \_ markov_chain.py       # Example CGI script (Python)
   \_ text
      \_ pass
         \_ fail               # Example text document
      \_ hackers.txt           # Example text document
      \_ lyrics.txt            # Example text document
      \_ song.txt              # Example text document
</pre>

---

### Diagrams
#### Server Workflow

1. Allocate a socket, bind it to a port, then listen for incoming connections
2. Accept an incoming client connection and parse the input data stream into a HTTP `request` structure
3. Based on the `request`'s parameters, form a response and send it back to the client
4. Continue to perform steps 2-3 for as long as the server is running
  - If in forking mode, fork after accepting a connection and let the child process handle parsing and responding to the request
  - If in single mode, simply handle one client at a time

![image](https://user-images.githubusercontent.com/67760716/106998307-223aae80-6739-11eb-86f8-689a47459e54.png)
#### File Structure

![image](https://user-images.githubusercontent.com/67760716/106998180-f1f31000-6738-11eb-921f-56482e5953fa.png)

---

### Usage
#### Server
<pre>
./bin/server [hcmMpr]
Options:
    -h  help       # Display help message
    -c  mode       # Single or Forking mode
    -m  path       # Path to mimetypes file
    -M  mimetype   # Default mimetype
    -p  port       # Port to listen on
    -r  path       # Root directory
</pre>
#### Test Script
<pre>
./bin/test.py [-h HAMMERS -t THROWS] URL
Options:
    -h  HAMMERS    # Number of hammers (processes) to utilize    (1)
    -t  THROWS     # Number of throws (HTTP requests) per hammer (1)
    -v             # Display verbose output
</pre>
