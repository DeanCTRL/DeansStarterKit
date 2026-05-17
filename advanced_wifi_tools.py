import subprocess
import re
import time
import os
from collections import defaultdict
from colorama import Fore, init

init(autoreset=True)

# --------------------------
# UTILITY FUNCTIONS
# --------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(Fore.YELLOW + "\nPress Enter to continue...")

# --------------------------
# WIFI SCANNING
# --------------------------
def scan_wifi():
    networks = []
    try:
        output = subprocess.check_output(
            "netsh wlan show networks mode=bssid",
            shell=True,
            text=True,
            errors="ignore"
        )
        lines = output.splitlines()
        current_ssid = None
        current_auth = None
        current_signal = None
        current_channel = None

        for line in lines:
            line = line.strip()
            if line.startswith("SSID") and "BSSID" not in line:
                parts = line.split(" : ")
                current_ssid = parts[1].strip() if len(parts) > 1 else "<Hidden Network>"
                if current_ssid == "":
                    current_ssid = "<Hidden Network>"
            elif "Authentication" in line:
                current_auth = line.split(":")[1].strip()
            elif "Signal" in line:
                current_signal = line.split(":")[1].strip()
            elif "Channel" in line:
                current_channel = line.split(":")[1].strip()
                networks.append({
                    "ssid": current_ssid,
                    "auth": current_auth,
                    "signal": current_signal,
                    "channel": current_channel
                })
    except Exception as e:
        print(Fore.RED + f"Error scanning WiFi: {e}")
    return networks

# --------------------------
# DISPLAY NETWORKS
# --------------------------
def display_networks(networks):
    print(Fore.CYAN + "\n--- WiFi Networks ---\n")
    for i, net in enumerate(networks, start=1):
        signal_int = int(net["signal"].replace("%","")) if net["signal"] else 0
        if signal_int >= 80: signal_color = Fore.GREEN
        elif signal_int >= 50: signal_color = Fore.YELLOW
        else: signal_color = Fore.RED
        security = Fore.GREEN + "SECURED" if "Open" not in net["auth"] else Fore.RED + "OPEN"
        print(Fore.BLUE + f"SSID       : {net['ssid']}")
        print(signal_color + f"Signal     : {net['signal']}")
        print(Fore.YELLOW + f"Channel    : {net['channel']}")
        print(Fore.MAGENTA + f"Encryption : {net['auth']}")
        print(f"Security   : {security}")
        print(Fore.CYAN + "-----------------------------")

# --------------------------
# LIVE SIGNAL GRAPH
# --------------------------
def signal_graph(networks):
    print(Fore.CYAN + "\n--- Live Signal Graph ---\n")
    for net in networks:
        try:
            signal_int = int(net["signal"].replace("%",""))
            bars = "█" * (signal_int // 5)
            print(Fore.BLUE + f"{net['ssid'][:20]:20} " + Fore.GREEN + bars + f" {signal_int}%")
        except:
            continue

# --------------------------
# DEVICE DISCOVERY
# --------------------------
def discover_devices():
    print(Fore.CYAN + "\nScanning local network for devices...\n")
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True, errors="ignore")
        devices = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})", output)
        if not devices:
            print(Fore.RED + "No devices discovered.")
            return
        vendor_dict = {
            "00-1A-2B": "Apple Device",
            "B8-27-EB": "Raspberry Pi",
            "FC-15-B4": "Samsung Device",
            "3C-5A-B4": "Xbox / Microsoft",
            "00-04-20": "PlayStation",
        }
        for ip, mac in devices:
            mac_prefix = mac.upper()[0:8]
            device_type = vendor_dict.get(mac_prefix, "Unknown")
            print(Fore.GREEN + f"IP       : {ip}")
            print(Fore.YELLOW + f"MAC      : {mac}")
            print(Fore.MAGENTA + f"TYPE     : {device_type}")
            print(Fore.CYAN + "-----------------------------")
    except Exception as e:
        print(Fore.RED + f"Error discovering devices: {e}")

# --------------------------
# WIFI MAP MODE
# --------------------------
def wifi_map(networks):
    print(Fore.CYAN + "\n--- WiFi Map Mode ---\n")
    channels = defaultdict(list)
    for net in networks:
        channels[net["channel"]].append(net["ssid"])
    for channel, ssids in channels.items():
        print(Fore.YELLOW + f"CHANNEL {channel}")
        for ssid in ssids:
            print(Fore.GREEN + f"  └── {ssid}")
        print()

# --------------------------
# AUTO REFRESH SCANNER
# --------------------------
def auto_refresh():
    while True:
        clear()
        networks = scan_wifi()
        display_networks(networks)
        signal_graph(networks)
        wifi_map(networks)
        print(Fore.RED + "\nPress CTRL+C to stop auto refresh")
        time.sleep(5)

# --------------------------
# WIFI MENU
# --------------------------
def wifi_menu():
    while True:
        clear()
        print(Fore.CYAN + "\n--- WiFi & Local Network Tools ---\n")
        print("1. Scan WiFi Networks")
        print("2. Live Signal Graph")
        print("3. Nearby Device Discovery")
        print("4. WiFi Map Mode")
        print("5. Auto Refresh Scanner")
        print("6. Return")
        choice = input(Fore.YELLOW + "Select option: ").strip()
        if choice == "1":
            nets = scan_wifi()
            display_networks(nets)
            pause()
        elif choice == "2":
            nets = scan_wifi()
            signal_graph(nets)
            pause()
        elif choice == "3":
            discover_devices()
            pause()
        elif choice == "4":
            nets = scan_wifi()
            wifi_map(nets)
            pause()
        elif choice == "5":
            auto_refresh()
        elif choice == "6":
            break
        else:
            print(Fore.RED + "Invalid option!")
            pause()

# --------------------------
# RUN MODULE DIRECTLY
# --------------------------
if __name__ == "__main__":
    wifi_menu()