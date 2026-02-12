import requests
import json
from colorama import init, Fore
from terminaltables import SingleTable

# Initialize colorama for Windows compatibility
init(autoreset=True)

# UI Icons
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
F = f"[{Fore.GREEN}+{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"

def bssid_finder():
    bssid = input(f"{Q} MAC/BSSID: ").strip()
    if not bssid:
        print(f"{W} Please enter a valid BSSID.")
        return

    print(f"\n{S} Locating '{bssid}'...")
    
    # Use a standard API URL with a timeout and User-Agent
    url = f"https://api.mylnikov.org/wifi?v=1.1&bssid={bssid}"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Kali/2024.1"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()      # Directly parse JSON
        
        result_code = data.get('result')

        if result_code == 200:
            lat = data['data'].get('lat')
            lon = data['data'].get('lon')
            location = f"{lat},{lon}"
            
            # Using terminaltables for a cleaner Kali-style output
            table_data = [
                ['BSSID', bssid],
                ['Coordinates', location],
                ['Google Maps', f"https://www.google.com/maps?q={location}"]
            ]
            table = SingleTable(table_data, " Results ")
            print("\n" + table.table)
            
        else:
            print(f"\n{W} Error {result_code}: Localization not found in database.")

    except requests.exceptions.RequestException as e:
        print(f"\n{W} Connection Error: {e}")
    except KeyError:
        print(f"\n{W} Data Error: Received unexpected response format.")

if __name__ == "__main__":
    bssid_finder()