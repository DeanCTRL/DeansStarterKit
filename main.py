# main.py
from colorama import Fore, init

# Import modules
from advanced_wifi_tools import wifi_menu
from osint_tools import osint_menu
from recon_tools import network_menu
from network_dashboard import show_network_dashboard
from dns_monitor import dns_monitor
from traffic_analytics import traffic_analytics
from exif_tools import exif_menu

init(autoreset=True)

def main_menu():
    while True:
        print(Fore.CYAN + "\n=== DEAN'S STARTER KIT ===\n")
        print(Fore.BLUE + "1. Advanced WiFi & Local Network Tools")
        print(Fore.GREEN + "2. OSINT Tools")
        print(Fore.MAGENTA + "3. Network Recon Tools")
        print(Fore.YELLOW + "4. Real-Time Network Dashboard")
        print(Fore.CYAN + "5. EXIF & File Metadata Tools")
        print(Fore.MAGENTA + "6. DNS / Domain Visibility")
        print(Fore.YELLOW + "7. Traffic Analytics / Top Talkers")
        print(Fore.RED + "8. Exit")

        choice = input(Fore.YELLOW + "\nSelect option: ").strip()

        if choice == "1":
            wifi_menu()
        elif choice == "2":
            osint_menu()
        elif choice == "3":
            network_menu()
        elif choice == "4":
            show_network_dashboard()
        elif choice == "5":
            exif_menu()
        elif choice == "6":
            print(Fore.CYAN + "\nStarting DNS/Domain Visibility monitor...")
            dns_monitor()
        elif choice == "7":
            print(Fore.CYAN + "\nStarting Traffic Analytics...")
            traffic_analytics()
        elif choice == "8":
            print(Fore.RED + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option! Try again.")

if __name__ == "__main__":
    main_menu()