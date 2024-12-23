import socket
import threading
import time

SYN_LIMIT = 5  # Maximum allowed SYN requests within the threshold time
TIME_WINDOW = 10  # Time window in seconds to track SYN requests
INACTIVITY_TIMEOUT = 10  # Timeout in seconds for waiting for handshake or payload

SDN_CONTROLLER_IP = "sdn-controller-service"  # SDN-controller IP (container name or IP address)
SDN_CONTROLLER_PORT = 9091  # Port where SDN-controller listens

syn_requests = {}

# Function to detect SYN flood attacks
def detect_syn_flood(client_ip):
    current_time = time.time()
    if client_ip not in syn_requests:
        syn_requests[client_ip] = []
    
    # Filter out old SYN timestamps outside of the time window
    syn_requests[client_ip] = [timestamp for timestamp in syn_requests[client_ip] if current_time - timestamp <= TIME_WINDOW]
    
    # Add the current timestamp for the new SYN packet
    syn_requests[client_ip].append(current_time)
    
    # If the client exceeds the SYN limit, it's considered a flood
    if len(syn_requests[client_ip]) > SYN_LIMIT:
        print(f"[SCM] SYN flood detected from {client_ip}. Dropping further requests.")
        return True
    return False

# Function to handle the client connection
def handle_client(client_socket, client_address):
    try:
        print(f"[SCM] Connection request from {client_address}")

        # Detect SYN flood
        if detect_syn_flood(client_address[0]):
            print(f"[SCM] Potential flood detected from {client_address[0]}. Dropping connection without responding.")
            client_socket.close()  # Close the socket without sending any SYN-ACK
            return

        # Set timeout for the handshake
        client_socket.settimeout(INACTIVITY_TIMEOUT)

        # Receive the SYN packet
        syn = client_socket.recv(4096)
        if syn != b"SYN":
            print(f"[SCM] Invalid handshake start from {client_address}. Dropping connection.")
            client_socket.close()
            return
        
        print(f"[SCM] Received SYN from {client_address}. Sending SYN-ACK.")
        client_socket.sendall(b"SYN-ACK")

        # Receive the ACK packet
        ack = client_socket.recv(4096)
        if ack != b"ACK":
            print(f"[SCM] Handshake failed with {client_address}. Dropping connection.")
            client_socket.close()
            return
        
        print(f"[SCM] Handshake successful with {client_address}. Forwarding to SDN controller...")

        # Establish a connection to SDN-controller
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sdn_socket:
            sdn_socket.connect((SDN_CONTROLLER_IP, SDN_CONTROLLER_PORT))
            print(f"[SCM] Connected to SDN Controller at {SDN_CONTROLLER_IP}:{SDN_CONTROLLER_PORT}")

            # Forward the data from client to SDN-controller
            while True:
                data = client_socket.recv(4096)
                if not data:
                    print(f"[SCM] Client {client_address} closed the connection.")
                    break

                print(f"[SCM] Forwarding data to SDN-controller: {data.decode()}")
                sdn_socket.sendall(data)  # Send to SDN controller

                # Wait for response from SDN-controller
                response = sdn_socket.recv(4096)
                if not response:
                    print(f"[SCM] No response from SDN-controller.")
                    break

                print(f"[SCM] Received response from SDN-controller: {response.decode()}")
                client_socket.sendall(response)  # Send back the response to the client

    except Exception as e:
        print(f"[SCM] Error: {e}")
    finally:
        client_socket.close()
        print(f"[SCM] Connection with {client_address} closed.")

# Function to start the SCM-proxy server
def start_scm_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("0.0.0.0", 9090))
        server.listen(5)
        print("[SCM] Listening on port 9090")
        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_scm_proxy()
