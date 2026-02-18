import requests
from colorama import init, Fore
from terminaltables import SingleTable
from urllib.parse import quote

# Core imports
from core.searchPJ import searchPJ
from core.searchPageDor import searchPageDor
from core.searchLocalCH import searchLocalCH
from core.searchYellowLU import searchYellowLU
from core.searchCopainsdavant import searchCopainsdavant
from core.searchPersonneLinkedin import searchPersonneLinkedin
from core.facebookSearchTool import facebookSearchTool
from core.twitterSearchTool import twitterSearchTool
from core.instagramSearchTool import instagramSearchTool

init(autoreset=True)

# UI Icons
W, Q, F, S = f"[{Fore.RED}!{Fore.RESET}]", f"[{Fore.YELLOW}?{Fore.RESET}]", f"[{Fore.GREEN}+{Fore.RESET}]", f"[{Fore.MAGENTA}*{Fore.RESET}]"

def search_personne(country_code):
    nom = input(f"{Q} Nom, Prénom: ").strip()
    city = input(f"{Q} Ville/Departement: ").strip()
    
    if not nom:
        print(f"{W} Le nom est requis.")
        return

    print(f"\n{S} Lancement de la recherche globale pour '{nom}'...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://google.com'
    }

    # --- 1. Regional Phone Books ---
    try:
        if country_code == 'FR' or country_code == 'ALL':
            url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quote(nom)}&ou={quote(city)}"
            res = requests.get(url, headers=headers, timeout=10)
            searchPJ(res)

        if country_code == 'BE' or country_code == 'ALL':
            url = f"https://www.pagesblanches.be/chercher/personne/{quote(nom)}/{quote(city)}/"
            res = requests.get(url, headers=headers, timeout=10)
            searchPageDor(res)

        if country_code == 'CH' or country_code == 'ALL':
            url = f"https://tel.local.ch/fr/q?area={quote(city)}&name={quote(nom)}&typeref=res"
            searchLocalCH(url)

        if country_code == 'LU' or country_code == 'ALL':
            url = f"https://www.yellow.lu/fr/pages-blanches/recherche?query={quote(nom)}"
            searchYellowLU(url)
    except Exception as e:
        print(f"{W} Erreur annuaires: {e}")

    # --- 2. Professional & School Networks ---
    searchCopainsdavant(nom, city)
    searchPersonneLinkedin(nom, city)

    # --- 3. Social Media Dispatchers ---
    
    # FACEBOOK
    fb = facebookSearchTool()
    fb_results = fb.searchFacebook(nom)
    if fb_results:
        table_fb = [('Name', 'User', 'Location')]
        for username, name in fb_results:
            # Note: Optional deep info check - can be slow
            # fb.getInfoProfile(username)
            table_fb.append((name, username, "See Profile"))
        print("\n" + SingleTable(table_fb, " Facebook ").table)

    # TWITTER
    tw = twitterSearchTool()
    tw_results = tw.searchTwitter(nom)
    if tw_results:
        table_tw = [('Name', 'User', 'Location')]
        for username, name in tw_results:
            # We skip getInfoProfile here to maintain tool speed
            table_tw.append((name, f"@{username}", "Dork Link"))
        print("\n" + SingleTable(table_tw, " Twitter ").table)

    # INSTAGRAM
    insta = instagramSearchTool()
    insta.search_insta(nom) # Using our optimized method
    if insta.accounts:
        table_insta = [('User', 'Link')]
        for acc in insta.accounts[:10]: # Limit to top 10 for speed
            table_insta.append((acc, f"instagram.com/{acc}"))
        print("\n" + SingleTable(table_insta, " Instagram ").table)

if __name__ == "__main__":
    search_personne("FR")


def searchPersonne(country_code):
    return search_personne(country_code)