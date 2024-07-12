# Uncomment this to pass the first stage
import socket
import re
import threading


def request_handler(conn: socket.socket):
    """ Function that handles client request """
    request = conn.recv(1024).decode() # decode bytes to string
    url = re.search("GET (.*) HTTP", request).group(1) # get first match of this regex search to get the req url

    if url == "/":
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif url.startswith("/echo/"):
        echo_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(url[6:])}\r\n\r\n{url[6:]}".encode()
        conn.sendall(echo_response)
    elif url.startswith("/user-agent"):
        user_agent = re.search("User-Agent: (.*)\r\n", request).group(1)
        user_agent_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
        conn.sendall(user_agent_response)
    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    conn.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, _ = server_socket.accept()
        thread = threading.Thread(target=request_handler, args=(conn,))
        thread.start()


if __name__ == "__main__":
    main()
