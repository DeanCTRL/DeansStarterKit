from PIL import Image
from PIL.ExifTags import TAGS
from colorama import Fore, init

init(autoreset=True)


def extract_exif():

    image_path = input(
        Fore.YELLOW +
        "Enter image path: "
    )

    try:

        image = Image.open(image_path)

        exif_data = image._getexif()

        if not exif_data:

            print(Fore.RED + "No EXIF data found")
            return

        print(Fore.CYAN + "\n========== EXIF DATA ==========\n")

        for tag_id, value in exif_data.items():

            tag = TAGS.get(tag_id, tag_id)

            print(Fore.GREEN + f"{tag}: {value}")

    except Exception as e:

        print(Fore.RED + f"Error: {e}")



def exif_menu():

    while True:

        print(Fore.CYAN + "\n========== EXIF TOOLS ==========")
        print("1. Extract EXIF Data")
        print("2. Return")

        choice = input(Fore.YELLOW + "\nSelect option: ").strip()

        if choice == "1":

            extract_exif()

        elif choice == "2":

            break