# -*- coding: utf-8 -*-
from core.LinkedIn import searchLinkedIn
from colorama import init, Fore
from terminaltables import SingleTable

# Initialize colorama with autoreset to avoid manual Fore.RESET
init(autoreset=True)

# UI Icons using f-strings
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
F = f"[{Fore.GREEN}+{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"

def employee_lookup():
    # .strip() prevents leading/trailing spaces from breaking the search
    enterprise = input(f"{Q} Enterprise: ").strip()
    city = input(f"{Q} Ville: ").strip()

    if not enterprise:
        print(f"{W} Enterprise name is required.")
        return

    print(f"\n{S} Recherche des employés de '{enterprise}' à '{city or 'Partout'}'...\n")

    try:
        # Initialize and perform search
        linkedin = searchLinkedIn()
        linkedin.search(enterprise, city)
        
        # Check if the search returned results
        if hasattr(linkedin, 'found') and linkedin.found:
            employees = getattr(linkedin, 'employees', [])
            
            if not employees:
                print(f"{W} Aucun employé trouvé.")
                return

            # Optimized Table Generation using List Comprehension
            table_data = [["Num", "Name"]]
            table_data.extend([[i + 1, name] for i, name in enumerate(employees)])

            table = SingleTable(table_data, title=f" LinkedIn: {enterprise} ")
            print(table.table)
            print(f"\n{F} Total trouvé: {len(employees)}")
        else:
            print(f"{W} Aucun résultat pour '{enterprise}'.")

    except Exception as e:
        print(f"{W} Une erreur est survenue lors de la recherche: {e}")

if __name__ == "__main__":
    employee_lookup()