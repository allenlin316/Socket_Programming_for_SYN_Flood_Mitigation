import socket

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                print("[TCP Server] Client closed the connection.")
                break
            print(f"[TCP Server] Received data: {data.decode()}")
            response = b"Response from TCP server"
            client_socket.sendall(response)
    except Exception as e:
        print(f"[TCP Server] Error: {e}")
    finally:
        client_socket.close()

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 9092))
        server.listen(5)
        print("[TCP Server] Listening on port 9092")
        while True:
            client_socket, client_address = server.accept()
            print(f"[TCP Server] Connection established with {client_address}")
            handle_client(client_socket)

if __name__ == "__main__":
    start_tcp_server()
