from scapy.all import *
import sys

# Ensure you provide a destination IP as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <target_ip>")
    sys.exit(1)

# Get the target IP from command-line argument
target_ip = sys.argv[1]

# Print the fields of the packet being sent
print("Field Values of packet sent")
packet = IP(dst=target_ip, id=1111, ttl=99) / TCP(sport=RandShort(), dport=[22, 80], seq=12345, ack=1000, window=1000, flags="S") / "HaX0r SVP"

# Send the packet and wait for responses
ans, unans = srloop(packet, inter=0.3, retry=2, timeout=4)

# Process the responses
def process_response(s, r):
    # Extract relevant information and print it in a readable format
    if r:  # If there is a response
        src_ip = s.dst  # Source IP address of the sent packet
        src_port = s.dport  # Source port of the sent packet
        dst_ip = r[IP].src  # Destination IP address from the received response
        dst_port = r[TCP].sport  # Destination port of the response
        ip_id = r[IP].id  # IP ID from the response
        ttl = r[IP].ttl  # TTL from the response
        tcp_flags = r[TCP].flags  # TCP flags in the response

        print(f"Response received from {dst_ip}:{dst_port} -> {src_ip}:{src_port}")
        print(f"IP ID: {ip_id}\tTTL: {ttl}\tTCP Flags: {tcp_flags}")
    else:
        # If no response, the target might be unresponsive (possible attacker)
        print(f"No response from {s.dst}:{s.dport}. Target might be an attacker.")

# Make a table of the responses
ans.make_table(lambda s, r: process_response(s, r))
