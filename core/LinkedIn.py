import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class SearchLinkedIn: # PascalCase for classes
    def __init__(self):
        # encrypted.google.com is deprecated; using standard google.com
        self.base_url = "https://www.google.com/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        # Common suffixes to strip from names
        self.suffixes = ["| LinkedIn", "on LinkedIn", "- LinkedIn", "LinkedIn", "…"]

    def search(self, company, city):
        """
        Performs Google Dorking to find LinkedIn profiles.
        """
        # Optimized Google Dork: site:linkedin.com/in "Company" "City"
        query = f'site:linkedin.com/in "{company}" "{city}"'
        params = {
            'q': query,
            'num': 100,
            'hl': 'en'
        }

        employee_list = []
        profiles_list = []

        try:
            res = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)
            if res.status_code == 200:
                # Use lxml parser for speed on Kali
                soup = BeautifulSoup(res.text, "lxml")
                
                # Modern Google result containers
                results = soup.select('div.g')

                for g in results:
                    # 1. Extract Name
                    h3 = g.select_one('h3')
                    if h3:
                        name = h3.get_text()
                        # Clean the name from LinkedIn suffixes
                        for suffix in self.suffixes:
                            name = name.replace(suffix, "")
                        employee_list.append(name.strip())

                    # 2. Extract Profile URL
                    link = g.select_one('a')
                    if link and 'href' in link.attrs:
                        url = link['href']
                        if "linkedin.com/in/" in url:
                            profiles_list.append(url)

        except Exception as e:
            print(f"Search Error: {e}")

        # Setting attributes for compatibility with your existing UI
        self.found = len(employee_list)
        self.employees = employee_list
        self.profiles = profiles_list


def searchLinkedIn():
    """Adapter for backward compatibility: returns a SearchLinkedIn instance."""
    return SearchLinkedIn()