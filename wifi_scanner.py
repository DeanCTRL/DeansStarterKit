import subprocess
import re
from colorama import Fore, init

init(autoreset=True)

def wifi_scan():

    print(Fore.CYAN + "\n==============================")
    print(Fore.BLUE + "   DEAN'S STARTER KIT")
    print(Fore.RED + "      WIFI SCANNER")
    print(Fore.CYAN + "==============================\n")

    try:

        output = subprocess.check_output(
            "netsh wlan show networks mode=bssid",
            shell=True,
            text=True,
            errors="ignore"
        )

        ssids = re.findall(r"SSID \d+ : (.*)", output)
        auths = re.findall(r"Authentication\s+: (.*)", output)
        signals = re.findall(r"Signal\s+: (.*)%", output)

        if not ssids:
            print(Fore.RED + "No WiFi networks found.\n")
            return

        print(Fore.YELLOW + f"Networks Found: {len(ssids)}\n")

        for i in range(len(ssids)):

            ssid = ssids[i].strip()

            auth = auths[i].strip() if i < len(auths) else "Unknown"

            signal = signals[i].strip() if i < len(signals) else "0"

            signal_int = int(signal)

            # Signal colors
            if signal_int >= 80:
                signal_color = Fore.GREEN
            elif signal_int >= 50:
                signal_color = Fore.YELLOW
            else:
                signal_color = Fore.RED

            # Encryption check
            if "Open" in auth:
                security = Fore.RED + "UNSECURED"
            else:
                security = Fore.GREEN + "SECURED"

            print(Fore.CYAN + "-----------------------------------")
            print(Fore.BLUE + f"SSID       : {ssid}")
            print(signal_color + f"Signal     : {signal}%")
            print(Fore.MAGENTA + f"Encryption : {auth}")
            print(f"Security   : {security}")

        print(Fore.CYAN + "\nScan Complete.\n")

    except Exception as e:

        print(Fore.RED + f"\nError scanning WiFi: {e}\n")


if __name__ == "__main__":
    wifi_scan()

    input(Fore.YELLOW + "Press Enter to exit...")