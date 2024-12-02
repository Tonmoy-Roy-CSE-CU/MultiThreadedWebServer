# Multithreaded Web Server

## Project Overview
The **Multithreaded Web Server** is implemented in Python. It is designed to handle multiple client requests simultaneously, serving static files from the server's file system. This lightweight server provides essential functionality for hosting static files, including HTML pages, CSS, JavaScript, and images.

---

## Key Features
- **Concurrent Client Handling**: Efficiently handles multiple client connections using threads, ensuring high concurrency.
- **Static File Serving**: Serves HTML, CSS, JavaScript, images, and other static files directly to clients.
- **Basic HTTP Support**: Supports simple HTTP GET requests, enabling clients to retrieve server resources.
- **Request Logging**: Logs client IP addresses, requested resources, and response statuses to a log file for tracking access history.
- **Error Handling**: Responds with appropriate HTTP error codes for missing or restricted files, including:
  - `404 Not Found`: When a requested file is not found.
  - `500 Internal Server Error`: For server-side issues.
- **Resource Synchronization**: Ensures thread-safe access to shared resources, preventing data conflicts in concurrent environments.
- **Dynamic Content**: Generates dynamic content such as the current date, time, or a digital clock using a REST API or custom HTML pages.

---
## Concurrent Testing with ApacheBench

### Making a GET request to our server

Run the following command in your terminal, in the directory where your `ab` and `abs` executable files are located:

```bash
./ab -c 10 -n 20 http://localhost:8080/
```
-c Concurrency: 
This indicates the number of multiple requests to make at a time. For this test, we are sending 10 requests to our server concurrently at the same time.

-n Request: 
This indicates the number of requests to perform. For this test, we are sending 20 requests in total.

For more information, visit the [Apache Benchmark documentation](https://httpd.apache.org/docs/2.4/programs/ab.html).

---
## How to Use
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/multithreaded-web-server.git
   cd multithreaded-web-server
