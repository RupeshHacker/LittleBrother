import requests
from urllib.parse import quote
from colorama import init, Fore

# Local imports
from core.searchLocalCH import searchLocalCH
from core.searchYellowLU import searchYellowLU
from core.searchPJ import searchPJ

init(autoreset=True)

# UI Icons
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
F = f"[{Fore.GREEN}+{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"

def search_address(country_code):
    """
    Look up addresses in French, Swiss, or Luxembourgish phone books.
    """
    address = input(f"{Q} Adresse (ex: 12 rue de la Paix, Paris): ").strip()
    
    if not address:
        print(f"{W} L'adresse ne peut pas être vide.")
        return

    print(f"\n{S} Recherche de '{address}' dans les annuaires [{country_code}]...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    # Helper function to prevent repetitive code
    def lookup_france(addr):
        # quote() ensures spaces like "Paris 75001" become "Paris%2075001"
        url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui=&ou={quote(addr)}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            searchPJ(res)
        except Exception as e:
            print(f"{W} Erreur PagesJaunes: {e}")

    def lookup_switzerland(addr):
        url = f"https://tel.local.ch/fr/q?ext=1&name=&company=&street={quote(addr)}&city=&area="
        try:
            # Note: searchLocalCH might need the response or just the URL depending on your core implementation
            searchLocalCH(url) 
        except Exception as e:
            print(f"{W} Erreur Local.ch: {e}")

    def lookup_luxembourg(addr):
        try:
            # Assuming searchYellowLU takes the address directly or handles its own requests
            searchYellowLU(addr)
        except Exception as e:
            print(f"{W} Erreur Yellow.lu: {e}")

    # Dispatcher Logic
    if country_code == "FR":
        lookup_france(address)
    elif country_code == "CH":
        lookup_switzerland(address)
    elif country_code == "LU":
        lookup_luxembourg(address)
    else:
        # If no specific country, try all available (standard OSINT behavior)
        print(f"{S} Code pays inconnu ou 'ALL' - Tentative sur tous les services...")
        lookup_france(address)
        lookup_switzerland(address)
        lookup_luxembourg(address)


def searchAdresse(country_code):
    return search_address(country_code)