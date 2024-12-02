import socket
import threading
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json  # Import the missing json module

# Server Configuration
HOST = '127.0.0.1'
PORT = 8080
WEB_ROOT = "static"  # Directory to serve files from
MAX_THREADS = 50     # Max number of concurrent threads in the pool
LOG_FILE = "server.log"

# Response Headers
HTTP_HEADERS = {
    "Content-Type": "text/html",
    "Server": "CustomPythonWebServer"
}

# File types and their corresponding MIME types
MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".txt": "text/plain"
}

def log_request(client_addr, method, path, status):
    """Logs request information to the console and to a log file."""
    log_message = f"{datetime.now()} - {client_addr[0]}:{client_addr[1]} - {method} {path} - {status}"
    print(log_message)
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_message + "\n")

def get_content_type(filepath):
    """Returns the Content-Type based on file extension."""
    ext = os.path.splitext(filepath)[1]
    return MIME_TYPES.get(ext, "application/octet-stream")

def handle_client(client_socket, client_addr):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return
        
        # Parse HTTP request
        headers = request.splitlines()
        request_line = headers[0].split()
        method, path = request_line[0], request_line[1]
        
        # Default to index.html for root path
        if path == "/":
            path = "/index.html"

        # Construct full file path
        filepath = WEB_ROOT + path

        # Check if file exists
        if os.path.isfile(filepath):
            # Open and read file content
            with open(filepath, 'rb') as file:
                response_body = file.read()
            
            # Create a 200 OK response
            status = "200 OK"
            content_type = get_content_type(filepath)
            content_length = len(response_body)
            response_header = f"HTTP/1.1 {status}\nContent-Type: {content_type}\nContent-Length: {content_length}\n\n"
        
        elif path == "/datetime":
            # Dynamic DateTime Page with Digital Clock and Day Name
            response_body = b"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Digital Clock</title>
                <style>
                     body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                        color: #fff;
                    }
                    .clock {
                        text-align: center;
                        background: rgba(0, 0, 0, 0.3);
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
                    }
                    .clock h1 {
                     font-size: 4rem;
                     margin: 0 0 10px 0;
                    }
                    .clock p {
                        font-size: 2rem;
                        margin: 5px 0;
                    }
                </style>
            </head>
            <body>
               <div class="clock">
                  <h1 id="time">Loading...</h1>
                  <p id="day">Loading...</p>
              </div>
              <script>
                  function updateClock() {
                      const now = new Date();
                      const timeString = now.toLocaleTimeString([], { hour12: false });
                      const dayName = now.toLocaleDateString('en-US', { weekday: 'long' });
                      const dateString = now.toLocaleDateString();
                      document.getElementById('time').textContent = timeString;
                      document.getElementById('day').textContent = `${dayName}, ${dateString}`;
                  }
                  // Update the clock immediately and then every second
                  updateClock();
                  setInterval(updateClock, 1000);
              </script>
            </body>
            </html>
            """
            status = "200 OK"
            response_header = f"HTTP/1.1 {status}\nContent-Type: text/html\n\n"
            client_socket.sendall(response_header.encode('utf-8') + response_body)
            log_request(client_addr, method, path, status)
            return

        elif path == "/api/time":
            # JSON API Response
            now = datetime.now()
            response_body = json.dumps({
                "date": now.strftime('%Y-%m-%d'),
                "time": now.strftime('%H:%M:%S')
            }).encode('utf-8')
            status = "200 OK"
            content_length = len(response_body)
            response_header = f"HTTP/1.1 {status}\nContent-Type: application/json\nContent-Length: {content_length}\n\n"
            client_socket.sendall(response_header.encode('utf-8') + response_body)
            log_request(client_addr, method, path, status)
            return

        else:
            # Handle 404
            path2 = "/404.html"
            filepath = WEB_ROOT + path2
            
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as file:
                    response_body = file.read()
            else:
                response_body = b"<h1>404 Not Found</h1>"
            
            status = "404 Not Found"
            content_length = len(response_body)
            response_header = f"HTTP/1.1 404 Not Found\nContent-Type: text/html\nContent-Length: {content_length}\n\n"
        
        # Send response header and body
        client_socket.sendall(response_header.encode('utf-8') + response_body)
        log_request(client_addr, method, path, status)

    except Exception as e:
        # Internal server error handling
        print(f"Error handling client {client_addr}: {e}")
        response_body = b"<h1>500 Internal Server Error</h1>"
        response_header = "HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\n"
        client_socket.sendall(response_header.encode('utf-8') + response_body)
        log_request(client_addr, "ERROR", "N/A", "500 Internal Server Error")

    finally:
        client_socket.close()


class MultiThreadedWebServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

    def start(self):
        # Use a thread pool to manage concurrency
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            print("Waiting for connections...")
            while True:
                client_socket, client_addr = self.server_socket.accept()
                print(f"Connection from {client_addr} accepted.")
                # Submit a new task to the thread pool for each client connection
                executor.submit(handle_client, client_socket, client_addr)

# Ensure the static directory exists and create a default index.html if not found
if not os.path.isdir(WEB_ROOT):
    os.makedirs(WEB_ROOT)
    with open(os.path.join(WEB_ROOT, "index.html"), "w") as f:
        f.write("<h1>Welcome to CustomPythonWebServer!</h1>")

# Run the server
if __name__ == "__main__":
    server = MultiThreadedWebServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.server_socket.close()
