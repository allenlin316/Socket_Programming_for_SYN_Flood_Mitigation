import socket

def user_client():
    scm_ip = "scm-proxy-service"  # Ensure this is the correct service name or container IP
    scm_port = 9090

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((scm_ip, scm_port))
            print("[Client] Connected to SCM Proxy.")

            # Simulate three-way handshake
            print("[Client] Sending SYN...")
            client_socket.sendall(b"SYN")
            response = client_socket.recv(4096)
            print(f"[Client] Received: {response.decode()}")

            if response == b"SYN-ACK":
                print("[Client] Sending ACK...")
                client_socket.sendall(b"ACK")

                # Enter a loop to type messages
                while True:
                    payload = input("[Client] Enter a message (or 'exit' to quit): ")
                    if payload.lower() == "exit":
                        print("[Client] Closing connection.")
                        break

                    print(f"[Client] Sending payload: {payload}")
                    client_socket.sendall(payload.encode())

                    # Wait for the response
                    response = client_socket.recv(4096)
                    if not response:
                        print("[Client] Server closed the connection.")
                        break
                    print(f"[Client] Received response: {response.decode()}")
            else:
                print("[Client] Handshake failed.")
    except Exception as e:
        print(f"[Client] Error: {e}")

if __name__ == "__main__":
    user_client()
