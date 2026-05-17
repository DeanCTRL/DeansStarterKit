import asyncio
import aiohttp
import hashlib
import requests
import phonenumbers
import webbrowser
import urllib.parse
import dns.resolver

from phonenumbers import geocoder, carrier
from colorama import Fore, init

init(autoreset=True)

# =========================================
# EMAIL LOOKUP
# =========================================

def email_lookup():

    email = input(
        Fore.YELLOW +
        "Enter email to lookup: "
    ).strip()

    if "@" not in email or "." not in email:

        print(
            Fore.RED +
            "Invalid email format"
        )

        return

    domain = email.split("@")[1]

    print(
        Fore.GREEN +
        f"\nDomain: {domain}"
    )

    # ---------------------------------
    # HIBP CHECK
    # ---------------------------------

    try:

        url = (
            "https://haveibeenpwned.com/"
            f"unifiedsearch/{email}"
        )

        r = requests.get(
            url,
            headers={
                "User-Agent": "DeanToolkit/1.0"
            },
            timeout=10
        )

        if r.status_code == 200:

            print(
                Fore.RED +
                f"⚠ {email} appears in breach data"
            )

        elif r.status_code == 404:

            print(
                Fore.GREEN +
                "No breaches found"
            )

        else:

            print(
                Fore.YELLOW +
                "Could not verify breach status"
            )

    except:

        print(
            Fore.RED +
            "HIBP connection failed"
        )

    # ---------------------------------
    # GRAVATAR CHECK
    # ---------------------------------

    try:

        hash_email = hashlib.md5(
            email.strip().lower().encode()
        ).hexdigest()

        gravatar_url = (
            f"https://www.gravatar.com/"
            f"{hash_email}.json"
        )

        r = requests.get(
            gravatar_url,
            timeout=10
        )

        if r.status_code == 200:

            print(
                Fore.GREEN +
                "Gravatar profile found"
            )

        else:

            print(
                Fore.RED +
                "No Gravatar profile"
            )

    except:

        print(
            Fore.RED +
            "Gravatar check failed"
        )

    # ---------------------------------
    # MX RECORD CHECK
    # ---------------------------------

    try:

        answers = dns.resolver.resolve(
            domain,
            'MX'
        )

        print(
            Fore.GREEN +
            "\nMX Records:"
        )

        for rdata in answers:

            print(
                Fore.YELLOW +
                f" - {rdata.exchange}"
            )

    except:

        print(
            Fore.RED +
            "No MX records found"
        )


# =========================================
# PHONE LOOKUP
# =========================================

def phone_lookup():

    phone = input(
        Fore.YELLOW +
        "Enter phone number with country code: "
    ).strip()

    try:

        parsed = phonenumbers.parse(phone)

        print(
            Fore.GREEN +
            f"\nCountry: "
            f"{geocoder.description_for_number(parsed, 'en')}"
        )

        print(
            Fore.GREEN +
            f"Carrier: "
            f"{carrier.name_for_number(parsed, 'en')}"
        )

        print(
            Fore.GREEN +
            f"Valid Number: "
            f"{phonenumbers.is_valid_number(parsed)}"
        )

    except:

        print(
            Fore.RED +
            "Invalid phone number"
        )


# =========================================
# PHONE FOOTPRINT CHECK
# =========================================

def phone_footprint_check():

    phone = input(
        Fore.YELLOW +
        "Enter phone number with country code: "
    ).strip()

    encoded = urllib.parse.quote(phone)

    print(
        Fore.CYAN +
        "\n========== PHONE FOOTPRINT ==========\n"
    )

    searches = {

        "Google Search":
        f'https://www.google.com/search?q="{encoded}"',

        "Facebook Mentions":
        f'https://www.google.com/search?q="{encoded}"+site:facebook.com',

        "LinkedIn Mentions":
        f'https://www.google.com/search?q="{encoded}"+site:linkedin.com',

        "Twitter/X Mentions":
        f'https://www.google.com/search?q="{encoded}"+site:twitter.com',

        "Reddit Mentions":
        f'https://www.google.com/search?q="{encoded}"+site:reddit.com',

        "WhatsApp Link":
        f'https://wa.me/{phone.replace("+","")}',

        "Telegram Search":
        f'https://t.me/{phone.replace("+","")}'
    }

    for name, url in searches.items():

        print(
            Fore.GREEN +
            f"{name}:"
        )

        print(
            Fore.YELLOW +
            f"{url}\n"
        )

    open_links = input(
        Fore.CYAN +
        "Open links in browser? (y/n): "
    ).lower()

    if open_links == "y":

        for url in searches.values():

            webbrowser.open(url)

        print(
            Fore.GREEN +
            "\nOpened links in browser"
        )


# =========================================
# ASYNC USERNAME LOOKUP
# =========================================

async def check_platform(
    session,
    platform,
    url,
    keyword
):

    try:

        async with session.get(
            url,
            timeout=10
        ) as response:

            text = await response.text()

            if (
                response.status == 200
                and keyword.lower() in text.lower()
                and "not found" not in text.lower()
            ):

                print(
                    Fore.GREEN +
                    f"[FOUND] {platform}"
                )

                print(
                    Fore.YELLOW +
                    f"{url}\n"
                )

                return True

            else:

                print(
                    Fore.RED +
                    f"[NOT FOUND] {platform}"
                )

                return False

    except:

        print(
            Fore.RED +
            f"[ERROR] {platform}"
        )

        return False


async def async_username_lookup():

    username = input(
        Fore.YELLOW +
        "Enter username to scan: "
    ).strip()

    platforms = {

        "GitHub":
        f"https://github.com/{username}",

        "Instagram":
        f"https://www.instagram.com/{username}/",

        "Reddit":
        f"https://www.reddit.com/user/{username}/",

        "Twitter/X":
        f"https://twitter.com/{username}",

        "TikTok":
        f"https://www.tiktok.com/@{username}",

        "Snapchat":
        f"https://www.snapchat.com/add/{username}",

        "Steam":
        f"https://steamcommunity.com/id/{username}",

        "YouTube":
        f"https://www.youtube.com/@{username}",

        "Pinterest":
        f"https://www.pinterest.com/{username}/",

        "Twitch":
        f"https://www.twitch.tv/{username}",

        "Medium":
        f"https://medium.com/@{username}",

        "Patreon":
        f"https://www.patreon.com/{username}",

        "Tumblr":
        f"https://{username}.tumblr.com",

        "Roblox":
        f"https://www.roblox.com/users/profile?username={username}"
    }

    headers = {

        "User-Agent":
        (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
        )
    }

    async with aiohttp.ClientSession(
        headers=headers
    ) as session:

        tasks = [

            check_platform(
                session,
                platform,
                url,
                username
            )

            for platform, url
            in platforms.items()
        ]

        results = await asyncio.gather(*tasks)

    print(
        Fore.CYAN +
        f"\nTotal Profiles Found: "
        f"{sum(results)}\n"
    )


# =========================================
# OSINT MENU
# =========================================

def osint_menu():

    while True:

        print(
            Fore.CYAN +
            "\n========== OSINT TOOLS ==========\n"
        )

        print("1. Email Lookup")
        print("2. Phone Number Lookup")
        print("3. Phone Footprint Check")
        print("4. Advanced Username Lookup")
        print("5. Return\n")

        choice = input(
            Fore.YELLOW +
            "Select option: "
        ).strip()

        if choice == "1":

            email_lookup()

        elif choice == "2":

            phone_lookup()

        elif choice == "3":

            phone_footprint_check()

        elif choice == "4":

            asyncio.run(
                async_username_lookup()
            )

        elif choice == "5":

            break

        else:

            print(
                Fore.RED +
                "Invalid option!"
            )


# =========================================
# RUN DIRECTLY
# =========================================

if __name__ == "__main__":

    osint_menu()