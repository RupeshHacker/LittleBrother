import requests
import re
from bs4 import BeautifulSoup
from terminaltables import SingleTable
from urllib.parse import quote

def search_copains_davant(full_name, city):
    """
    Scrapes Copains d'Avant for people based on name and city.
    """
    # 1. Parse Name
    name_parts = full_name.split(" ", 1)
    prenom = name_parts[0] if len(name_parts) > 1 else ""
    nom = name_parts[1] if len(name_parts) > 1 else full_name

    # 2. Build and Execute Search Request
    base_url = "http://copainsdavant.linternaute.com/s/"
    params = f"?ty=1&prenom={quote(prenom)}&nom={quote(nom)}&ville={quote(city)}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Kali/2026.1'}
    
    try:
        res = requests.get(base_url + params, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"[!] Connection Error: {e}")
        return

    soup = BeautifulSoup(res.text, "lxml")
    
    # Identify result blocks
    # Each person is typically inside a block that contains their name and location
    results = soup.select('ul.app_list--result__search > li')
    
    table_data = [('Name', 'Location', 'Birth Date', 'Occupation', 'Profile ID')]
    found_count = 0

    for person in results:
        # Extract basic info from the search list
        name_tag = person.select_one('div.grid_last a')
        loc_tag = person.select_one('span.app_list--result__search__place')
        
        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)
        location = loc_tag.get_text(strip=True).split(" - ")[0] if loc_tag else "Unknown"
        profile_url = name_tag.get('href', '')
        profile_id = re.search(r'/p/([^/]+)', profile_url)
        profile_id = profile_id.group(1) if profile_id else "N/A"

        # 3. Deep Scrape Profile (Fetch Birthdate and Work)
        # Note: This can be slow if there are many results. We limit to first 10.
        birth_date = "N/A"
        work = "N/A"
        
        if profile_url and found_count < 10:
            try:
                p_res = requests.get(f"http://copainsdavant.linternaute.com{profile_url}", headers=headers, timeout=5)
                p_soup = BeautifulSoup(p_res.text, "lxml")
                
                # Use specific tags for Birthday and Job
                bday_tag = p_soup.select_one('abbr.bday')
                if bday_tag:
                    birth_date = bday_tag.get('title', '').split(' ')[0] # Extract YYYY-MM-DD
                
                job_tag = p_soup.select_one('p.title')
                if job_tag:
                    work = job_tag.get_text(strip=True)
            except:
                pass

        table_data.append((name, location, birth_date, work, profile_id))
        found_count += 1

    # 4. Display Results
    if found_count > 0:
        table = SingleTable(table_data, " Copains d'Avant Results ")
        print("\n" + table.table)
    else:
        print("[!] No results found for this name and city.")

if __name__ == "__main__":
    # Test call
    search_copains_davant("Jean Dupont", "Paris")