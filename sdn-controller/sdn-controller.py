import socket

TCP_SERVER_IP = "tcp-server-service"  # TCP server container name or IP address
TCP_SERVER_PORT = 9092  # Port where the TCP server listens

def forward_to_tcp_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((TCP_SERVER_IP, TCP_SERVER_PORT))
        print(f"[SDN] Forwarding data to TCP Server: {data.decode()}")
        tcp_socket.sendall(data)
        
        # Wait for the response from TCP server
        response = tcp_socket.recv(4096)
        print(f"[SDN] Received response from TCP Server: {response.decode()}")
        return response

def handle_sdn_connection(sdn_socket):
    try:
        while True:
            data = sdn_socket.recv(4096)
            if not data:
                print("[SDN] No data received. Closing connection.")
                break
            
            print(f"[SDN] Data received from SCM-proxy: {data.decode()}")
            response = forward_to_tcp_server(data)  # Forward data to TCP server
            sdn_socket.sendall(response)  # Send response back to SCM-proxy
    except Exception as e:
        print(f"[SDN] Error: {e}")
    finally:
        sdn_socket.close()

def start_sdn_controller():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 9091))  # Listening on port 9091
        server.listen(5)
        print("[SDN] Listening on port 9091")
        while True:
            sdn_socket, sdn_address = server.accept()
            print(f"[SDN] Connection established with {sdn_address}")
            handle_sdn_connection(sdn_socket)

if __name__ == "__main__":
    start_sdn_controller()
