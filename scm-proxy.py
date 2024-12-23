from scapy.all import *
from collections import Counter
from time import localtime, strftime, sleep
import threading
import logging

# Global variables
attack_flag = False
syn_count = Counter()
logging.basicConfig(filename='traffic_analysis.log', format='%(message)s', level=logging.INFO)

# Threshold for SYN packets per minute (e.g., 25 SYN packets per 3 seconds)
SYN_THRESHOLD = 25
TIME_WINDOW = 3  # Time window in seconds
CACHE_CLEAR_INTERVAL = 3.5  # Clear counter every 3.5 seconds

class ClearCacheThread(threading.Thread):
    def run(self):
        global attack_flag, syn_count

        while True:
            cur_time = strftime("%a, %d %b %Y %X", localtime())

            # Check if attack flag is triggered
            if attack_flag:
                logging.info(cur_time + " SYN attack detected! IP: " +
                             str(syn_count.most_common(1)[0][0]) + " No. of attempts: " +
                             str(syn_count.most_common(1)[0][1]))
                attack_flag = False  # Reset flag after logging the attack

            else:
                logging.info(cur_time + " Everything is normal")

            # Clear the SYN count for the next cycle
            syn_count.clear()
            sleep(CACHE_CLEAR_INTERVAL)


def flow_labels(pkt):
    global attack_flag

    if IP in pkt:
        ipsrc = str(pkt[IP].src)  # Source IP
        ipdst = str(pkt[IP].dst)  # Destination IP
        prtcl = pkt.getlayer(2).name  # Protocol (TCP/UDP)

        # Print flow information (if needed)
        flow = '{:<4} | {:<16} | {:<6} | {:<16} | '.format(prtcl, ipsrc, "", ipdst, "")
        # print(flow)

    # TCP SYN packet detection
    if TCP in pkt and pkt[TCP].flags & 2:  # Check for SYN flag (2 is the SYN flag)
        src = pkt.sprintf('{IP:%IP.src%}{IPv6:%IPv6.src%}')  # Get source IP address
        syn_count[src] += 1  # Increment SYN packet count for the source IP

        # Detect SYN flood if more than SYN_THRESHOLD attempts from the same IP
        if syn_count[src] > SYN_THRESHOLD and pkt.ack == 0:
            attack_flag = True  # Flag attack as detected


# Start the cache clearing thread
ClearCacheThread().start()

# Start sniffing network packets
sniff(prn=flow_labels, store=0)
