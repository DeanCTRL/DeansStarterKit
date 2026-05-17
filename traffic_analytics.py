# traffic_analytics.py
import psutil
import time
from colorama import Fore, init

init(autoreset=True)

def traffic_analytics():
    print(Fore.CYAN + "\n=== LOCAL TRAFFIC ANALYTICS ===")
    print(Fore.YELLOW + "Press Ctrl+C to stop.\n")

    try:
        while True:
            net_io = psutil.net_io_counters(pernic=True)
            conns = psutil.net_connections()

            print(Fore.CYAN + "==== Interface Stats ====")
            for iface, stats in net_io.items():
                print(Fore.GREEN + f"Interface: {iface}")
                print(Fore.YELLOW + f"Bytes Sent: {stats.bytes_sent / 1024:.2f} KB")
                print(Fore.YELLOW + f"Bytes Received: {stats.bytes_recv / 1024:.2f} KB")
                print(Fore.MAGENTA + f"Packets Sent: {stats.packets_sent}")
                print(Fore.MAGENTA + f"Packets Received: {stats.packets_recv}")
                print(Fore.WHITE + "-" * 40)

            # Active connections per IP
            local_ips = {}
            for c in conns:
                if c.laddr:
                    local_ips[c.laddr.ip] = local_ips.get(c.laddr.ip, 0) + 1

            print(Fore.CYAN + "\n==== Active Connections per IP ====")
            for ip, count in local_ips.items():
                print(Fore.GREEN + f"{ip}: {count} connections")

            # Top talkers (most connections)
            if local_ips:
                sorted_ips = sorted(local_ips.items(), key=lambda x: x[1], reverse=True)
                print(Fore.CYAN + "\n==== Top Talkers ====")
                for ip, count in sorted_ips[:5]:
                    print(Fore.YELLOW + f"{ip}: {count} connections")

            print(Fore.CYAN + "="*50 + "\n")
            time.sleep(5)  # refresh every 5 seconds

    except KeyboardInterrupt:
        print(Fore.RED + "\nStopped traffic analytics.")