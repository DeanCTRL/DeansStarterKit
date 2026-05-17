# recon_tools.py
import subprocess
import platform
import socket
import time
import threading
from colorama import Fore, init
from tqdm import tqdm
from mac_vendor_lookup import MacLookup

init(autoreset=True)

# Initialize MAC vendor lookup
mac_lookup = MacLookup()
try:
    mac_lookup.update_vendors()  # download latest IEEE OUI database
except:
    pass  # fallback if offline

# =========================================
# Vendor Detection
# =========================================
def get_vendor(mac):
    try:
        return mac_lookup.lookup(mac)
    except:
        return "Unknown Vendor"

# =========================================
# Device Type Detection
# =========================================
def detect_device_type(vendor, hostname):
    hostname = hostname.lower()
    if "iphone" in hostname:
        return "iPhone"
    elif "android" in hostname:
        return "Android Phone"
    elif "xbox" in hostname:
        return "Xbox"
    elif "playstation" in hostname:
        return "PlayStation"
    elif "tv" in hostname:
        return "Smart TV"
    elif "printer" in hostname:
        return "Printer"
    elif "desktop" in hostname:
        return "PC"
    elif "laptop" in hostname:
        return "Laptop"
    elif "macbook" in hostname:
        return "MacBook"
    elif "apple" in vendor.lower():
        return "Apple Device"
    elif "samsung" in vendor.lower():
        return "Samsung Device"
    return "Unknown"

# =========================================
# Hostname Lookup
# =========================================
def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "Unknown"

# =========================================
# Threaded Ping Sweep
# =========================================
def threaded_ping_sweep(base_ip):
    system_os = platform.system().lower()
    param = "-n" if system_os == "windows" else "-c"
    live_hosts = []

    def ping_ip(ip):
        try:
            result = subprocess.run(["ping", param, "1", ip],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            output = result.stdout.lower()
            if "ttl" in output or "bytes from" in output:
                live_hosts.append(ip)
        except:
            pass

    threads = []
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=ping_ip, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return live_hosts

# =========================================
# Subnet / Device Scan
# =========================================
def subnet_scan():
    # Detect local subnet
    local_ip = socket.gethostbyname(socket.gethostname())
    base_ip = ".".join(local_ip.split(".")[:3])
    print(Fore.CYAN + f"Pinging subnet {base_ip}.1-254 to wake devices...")

    live_hosts = threaded_ping_sweep(base_ip)

    print(Fore.CYAN + "\nScanning ARP cache for devices...\n")
    try:
        for _ in tqdm(range(100), desc="Scanning", ncols=75):
            time.sleep(0.01)

        # Read ARP cache
        result = subprocess.check_output("arp -a", shell=True, text=True, errors="ignore")
        lines = result.splitlines()
        devices = []

        for line in lines:
            if "-" in line and "." in line:
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    if live_hosts and ip not in live_hosts:
                        continue  # only show active hosts
                    mac = parts[1].replace("-", ":")
                    hostname = get_hostname(ip)
                    vendor = get_vendor(mac)
                    device_type = detect_device_type(vendor, hostname)
                    devices.append({
                        "ip": ip,
                        "mac": mac,
                        "hostname": hostname,
                        "vendor": vendor,
                        "device_type": device_type
                    })

        if not devices:
            print(Fore.RED + "\nNo devices found.")
            return

        print(Fore.CYAN + "\n========== DEVICES FOUND ==========\n")
        for device in devices:
            print(Fore.GREEN + f"IP: {device['ip']}")
            print(Fore.CYAN + f"Hostname: {device['hostname']}")
            print(Fore.MAGENTA + f"Vendor: {device['vendor']}")
            print(Fore.YELLOW + f"MAC: {device['mac']}")
            print(Fore.BLUE + f"Device Type: {device['device_type']}")
            print(Fore.WHITE + "-" * 40)

        print(Fore.GREEN + f"\nTotal Devices Found: {len(devices)}")

    except Exception as e:
        print(Fore.RED + f"Error: {e}")

# =========================================
# Live IP Tracker
# =========================================
def live_ip_tracker():
    local_ip = socket.gethostbyname(socket.gethostname())
    base_ip = ".".join(local_ip.split(".")[:3])
    print(Fore.CYAN + f"Monitoring subnet {base_ip}.1-254 ... Press Ctrl+C to stop.")
    system_os = platform.system().lower()
    param = "-n" if system_os == "windows" else "-c"

    try:
        while True:
            live_hosts = []
            for i in range(1, 255):
                ip = f"{base_ip}.{i}"
                try:
                    result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output = result.stdout.lower()
                    if "ttl" in output or "bytes from" in output:
                        live_hosts.append(ip)
                except Exception:
                    continue

            if live_hosts:
                print(Fore.GREEN + f"\nLive hosts ({len(live_hosts)}):")
                for host in live_hosts:
                    print(Fore.YELLOW + f" - {host}")
            else:
                print(Fore.RED + "\nNo live hosts detected.")

            time.sleep(10)

    except KeyboardInterrupt:
        print(Fore.RED + "\nStopped live IP monitoring.")

# =========================================
# Banner Grab
# =========================================
def banner_grab(ip):
    port_input = input(Fore.YELLOW + "Enter port to connect to (default 80): ").strip()
    port = int(port_input) if port_input else 80
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, port))
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore")
            except:
                banner = "No banner received"
        print(Fore.GREEN + f"Banner for {ip}:{port}\n{banner}")
    except Exception as e:
        print(Fore.RED + f"Could not connect to {ip}:{port} ({e})")

# =========================================
# Network Menu
# =========================================
def network_menu():
    while True:
        print(Fore.CYAN + "\n=== Network Recon Tools ===")
        print(Fore.GREEN + "1. Subnet / Device Scan")
        print(Fore.GREEN + "2. Live IP Tracker")
        print(Fore.GREEN + "3. Banner Grab")
        print(Fore.RED + "4. Return")

        choice = input(Fore.YELLOW + "Select option: ").strip()

        if choice == "1":
            subnet_scan()
        elif choice == "2":
            live_ip_tracker()
        elif choice == "3":
            ip = input(Fore.YELLOW + "Enter IP for banner grab: ").strip()
            banner_grab(ip)
        elif choice == "4":
            break
        else:
            print(Fore.RED + "Invalid option!")