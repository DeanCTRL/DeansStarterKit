# dns_monitor.py
from scapy.all import sniff, DNS, DNSQR
from colorama import Fore, init

init(autoreset=True)

def dns_monitor():  # <--- must match import in main.py
    """
    Capture DNS queries on your local network.
    """
    print(Fore.CYAN + "Starting DNS monitoring... Press Ctrl+C to stop.\n")

    def process_packet(packet):
        if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:  # qr=0 means query
            queried_domain = packet.getlayer(DNSQR).qname.decode()
            src_ip = packet[0][1].src
            print(Fore.GREEN + f"{src_ip} → {queried_domain}")

    sniff(filter="udp port 53", prn=process_packet)