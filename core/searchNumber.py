import requests
from colorama import init, Fore
from terminaltables import SingleTable

# Core imports
from core.searchPJ import searchPJ
from core.searchInfoNumero import searchInfoNumero
from core.searchLocalCH import searchLocalCH
from core.searchYellowLU import searchYellowLU

init(autoreset=True)

# UI Icons
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"

class PhoneSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://google.com'
        }

    def _show_info_table(self, num):
        """Helper to fetch and display technical phone info (Type, Operator, etc)"""
        phone = searchInfoNumero()
        phone.search(num)
        
        table_data = [
            ["Field", "Value"],
            ["Numéro", num],
            ["Type", phone.phone_type or "Inconnu"],
            ["Opérateur", phone.operator or "Inconnu"],
            ["Ville", phone.city or "Inconnu"],
            ["Localisation", phone.location or "Inconnu"]
        ]
        
        print("\n" + SingleTable(table_data, " Infos Techniques ").table)

    def search_france(self, num):
        url = f"https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui={num}"
        try:
            req = requests.get(url, headers=self.headers, timeout=10)
            searchPJ(requete=req, num=num)
            self._show_info_table(num)
        except Exception as e:
            print(f"{W} Erreur PagesJaunes: {e}")

    def search_switzerland(self, num):
        url = f"https://tel.local.ch/fr/q?ext=1&rid=NV3M&name=&company=&street=&city=&area=&phone={num}"
        searchLocalCH(url)

    def search_luxembourg(self, num):
        url = f"https://www.yellow.lu/fr/annuaire-inverse/recherche?query={num}"
        searchYellowLU(url)

def searchNumber(codemonpays):
    num = input(f"{Q} Téléphone: ").strip()
    if not num: return

    searcher = PhoneSearcher()
    print(f"\n{S} Recherche inversée pour '{num}' [{codemonpays}]...")

    # Logic Dispatcher
    if codemonpays == "FR":
        searcher.search_france(num)
    elif codemonpays == "CH":
        searcher.search_switzerland(num)
    elif codemonpays == "LU":
        searcher.search_luxembourg(num)
    else:
        # If 'ALL' or unknown, run all services without repeating code
        print(f"{S} Scan Global activé...")
        searcher.search_france(num)
        searcher.search_switzerland(num)
        searcher.search_luxembourg(num)