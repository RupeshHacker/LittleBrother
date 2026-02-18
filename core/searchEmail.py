import requests
import re
from colorama import init, Fore
from terminaltables import SingleTable
from core.leaked import Leaked  # Using the optimized Leaked class we created

init(autoreset=True)

# UI Icons
W, Q, F, S = f"[{Fore.RED}!{Fore.RESET}]", f"[{Fore.YELLOW}?{Fore.RESET}]", f"[{Fore.GREEN}+{Fore.RESET}]", f"[{Fore.MAGENTA}*{Fore.RESET}]"

def search_email_leaks():
    email = input(f"{Q} Email: ").strip()
    if not email: return

    print(f"\n{S} Recherche de fuites (HIBP) pour '{email}'...")
    
    # 1. Check Breach Databases (HIBP)
    lkd = Leaked(hibp_api_key="YOUR_KEY_HERE") # Needs your API key now
    breaches = lkd.check_email_breach(email)

    if isinstance(breaches, list) and breaches:
        table_data = [['Title', 'Domain', 'Date']]
        table_data.extend([[b['Title'], b['Domain'], b['Date']] for b in breaches])
        print("\n" + SingleTable(table_data, " Sites Compromis ").table)
    else:
        print(f"{W} Aucune brèche publique trouvée via API.")

    # 2. Google Dorking for "Combo Lists" (Passwords)
    print(f"\n{S} Recherche de mots de passe (Dorking)...")
    
    # Dork: intext:"user@email.com:" looks for "email:password" format
    search_url = "https://www.google.com/search"
    params = {'q': f'intext:"{email}:"', 'num': 50}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

    try:
        res = requests.get(search_url, params=params, headers=headers, timeout=10)
        # Using a set to avoid duplicate passwords
        found_combos = set()
        
        # Simple extraction of URLs from search results
        links = re.findall(r'url\?q=(https?://.*?)&', res.text)
        links = [l for l in links if not any(x in l for x in ["google", "youtube", "facebook"])]

        if not links:
            print(f"{W} Aucun dump public trouvé sur Google.")
            return

        print(f"{S} Analyse de {len(links)} sources potentielles...")

        for link in links:
            try:
                # Scrape the text content of the potential dump
                page_text = requests.get(link, headers=headers, timeout=5).text
                
                # Regex logic: find the email followed by a colon and then the password
                # This pattern stops at whitespace or common HTML delimiters
                pattern = f"{re.escape(email)}:([^\\s<>\"]+)"
                matches = re.findall(pattern, page_text)
                
                for password in matches:
                    found_combos.add(password)
            except:
                continue

        if found_combos:
            dump_table = [['Email', 'Password']]
            dump_table.extend([[email, pwd] for pwd in found_combos])
            print("\n" + SingleTable(dump_table, " Dumps Trouvés ").table)
        else:
            print(f"{W} Aucun mot de passe en clair trouvé.")

    except Exception as e:
        print(f"{W} Erreur lors du Dorking: {e}")

if __name__ == "__main__":
    search_email_leaks()


def SearchEmail():
    """Compatibility wrapper expected by the main menu."""
    return search_email_leaks()