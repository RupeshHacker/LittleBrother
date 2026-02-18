from bs4 import BeautifulSoup
from terminaltables import SingleTable
from core.searchInfoNumero import searchInfoNumero
from colorama import Fore

# Assuming icons are defined globally in your main script, otherwise:
W = f"[{Fore.RED}!{Fore.RESET}]"

def search_page_dor(request, num=''):
    """
    Parses Pages d'Or (Belgium) results and displays them in a table.
    """
    if not request or 'Aucun résultat' in request.text:
        print(f"\n{W} Aucun résultat pour votre recherche... o_o'")
        return

    # Use lxml for faster parsing on Kali
    soup = BeautifulSoup(request.text, "lxml")
    
    # Standardized extraction using CSS selectors
    # These containers usually hold the name, address, and phone together
    results = soup.select('div.result-item') # Adjust this selector based on current site structure
    
    table_data = [('Name', 'Adresse', 'Phone', 'Operateur')]
    found_any = False

    # Initialize Info tool once outside the loop
    phone_tool = searchInfoNumero()

    # If the specific selectors in your original code are correct:
    names = [n.get_text(strip=True) for n in soup.find_all("h2", {"class": "result-item-title"})]
    addresses = [a.get_text(strip=True) for a in soup.find_all("li", {"class": "address"})]
    numbers = [p.get_text(strip=True) for p in soup.find_all("li", {"class": "phone"})]

    # Zip them together to maintain data integrity
    for name, addr, phone_val in zip(names, addresses, numbers):
        found_any = True
        
        # Optional: Only lookup operator if needed to save time
        # phone_tool.search(phone_val)
        # operator = phone_tool.operator or "Inconnu"
        operator = "Check Tech Info" # Placeholder to keep the tool fast

        table_data.append((name, addr, phone_val, operator))

    if found_any:
        table = SingleTable(table_data, " Particulier (BE) ")
        print("\n" + table.table)
    else:
        # Fallback if the lists were empty but "Aucun résultat" wasn't in text
        print(f"\n{W} La structure de la page a changé ou aucun résultat n'est visible.")


def searchPageDor(request, num=''):
    """Compatibility wrapper for existing imports."""
    return search_page_dor(request, num=num)