# import socket module
from socket import *
import sys


def webServer(port=13331):
    # Create TCP server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Allow quick restart on the same port
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print("Ready to serve...")
        connectionSocket, addr = serverSocket.accept()

        try:
            message_bytes = connectionSocket.recv(4096)
            if not message_bytes:
                connectionSocket.close()
                continue

            message = message_bytes.decode("iso-8859-1", errors="replace")
            # Example request line: GET /index.html HTTP/1.1
            parts = message.split()
            if len(parts) < 2:
                raise ValueError("Malformed request")

            method = parts[0].upper()
            path = parts[1]

            # Only handle GET for this lab
            if method != "GET":
                body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
                status_line = b"HTTP/1.1 405 Method Not Allowed\r\n"
                headers = (
                    b"Content-Type: text/html; charset=UTF-8\r\n"
                    + f"Content-Length: {len(body)}\r\n".encode("ascii")
                    + b"Connection: close\r\n"
                    + b"\r\n"
                )
                connectionSocket.sendall(status_line + headers + body)
                connectionSocket.close()
                continue

            # Map "/" to a default file if you want; otherwise it will 404.
            if path == "/":
                filename = "index.html"
            else:
                # Strip leading slash
                filename = path.lstrip("/")

            # Read the requested file (binary-safe)
            with open(filename, "rb") as f:
                body = f.read()

            status_line = b"HTTP/1.1 200 OK\r\n"
            headers = (
                b"Content-Type: text/html; charset=UTF-8\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Connection: close\r\n"
                + b"\r\n"
            )

            # Send everything at once (status line + headers + blank line + body)
            connectionSocket.sendall(status_line + headers + body)
            connectionSocket.close()

        except Exception:
            # 404 Not Found
            body = b"<html><body><h1>404 Not Found</h1></body></html>"
            status_line = b"HTTP/1.1 404 Not Found\r\n"
            headers = (
                b"Content-Type: text/html; charset=UTF-8\r\n"
                + f"Content-Length: {len(body)}\r\n".encode("ascii")
                + b"Connection: close\r\n"
                + b"\r\n"
            )
            connectionSocket.sendall(status_line + headers + body)
            connectionSocket.close()


if __name__ == "__main__":
    webServer(13331)
