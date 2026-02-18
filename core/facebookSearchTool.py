import requests
import re
import json
from urllib.parse import quote

class FacebookSearchTool: # PascalCase for classes

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def search_facebook(self, nom):
        # Use quote for proper URL encoding
        url = f"https://www.facebook.com/public/{quote(nom)}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.text
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return []

        # Use a set for urlsAccount to handle uniqueness automatically
        urls_account = set(re.findall(r'https://www\.facebook\.com/[\w\d\.-]+', data))
        # Better regex for names in alt tags
        names_account = re.findall(r'width="72" height="72" alt="([^"]+)"', data)

        # Filtering with a list comprehension is significantly faster
        exclude_keywords = {"/public/", "/login.php", "/recover", "/help/", "directory/", "login/", "&", "/pages/"}
        
        filtered_urls = [
            u for u in urls_account 
            if not any(key in u for key in exclude_keywords) and not u.endswith('s')
        ]

        # Cleanup usernames: avoid multiple loops
        usernames = [u.replace("https://www.facebook.com/", "") for u in filtered_urls if u.count("/") <= 3]
        
        return zip(usernames, names_account)

    def get_info_profile(self, profile):
        url = f"https://www.facebook.com/{profile}" if "http" not in profile else profile
        username = url.rstrip('/').split('/')[-1]

        # Reset attributes
        self.facebook_id = self.name = self.profile = self.username = self.job = self.address = self.affiliations = None

        try:
            page = requests.get(url, headers=self.headers, timeout=10).text
            
            # Extract ID more reliably
            id_match = re.search(r'"entity_id":"(\d+)"|entity_id=(\d+)', page)
            self.facebook_id = id_match.group(1) or id_match.group(2) if id_match else None

            # Extract JSON-LD data
            json_match = re.search(r'type="application/ld\+json">(.*?)</script>', page)
            if json_match:
                values = json.loads(json_match.group(1))
                
                self.name = values.get('name')
                self.profile = url
                self.username = username
                self.job = values.get('jobTitle')
                self.address = values.get('address', {}).get('addressLocality')
                
                # Use list comprehension for affiliations instead of while loop
                affiliations = values.get('affiliation', [])
                self.affiliations = [a.get('name') for a in affiliations if 'name' in a]

        except Exception as e:
            print(f"Erreur profile {username}: {e}")

    # Backwards-compatible aliases
    def getInfoProfile(self, profile):
        return self.get_info_profile(profile)


def facebookSearchTool():
    """Factory for backward compatibility: returns a FacebookSearchTool instance."""
    return FacebookSearchTool()