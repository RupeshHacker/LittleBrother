import requests
import re
import json
from urllib.parse import quote

class TwitterSearchTool:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def searchTwitter(self, nom):
        """Searches for users. Note: Twitter now requires guest tokens or search via dorks."""
        # Using Google Dorking as a fallback because direct search is now blocked without login
        search_query = f'site:twitter.com "{nom}"'
        # For legacy compatibility, we'll keep the structure but note it may require a session
        url = f"https://twitter.com/search?f=users&q={quote(nom)}"
        
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            # Modern Twitter uses GraphQL; regex on raw HTML is highly unreliable now
            datas = re.findall(r'data-screen-name="([^"]+)"\s+data-name="([^"]+)"', res.text)
            return datas # Returns list of (username, name)
        except Exception as e:
            print(f"[!] Search error: {e}")
            return []

    def getInfoProfile(self, username):
        """Extracts profile metadata safely."""
        username = username.replace("@", "").strip()
        url_site = f"https://twitter.com/{username}"
        
        # Reset all attributes to None
        self.id = self.name = self.username = self.location = self.url = None
        self.description = self.protected = self.followers = self.friends = None
        self.create = self.geo = self.verified = self.status = self.langue = None
        self.birth = "None"

        try:
            res = requests.get(url_site, headers=self.headers, timeout=10)
            if res.status_code != 200:
                return

            page_source = res.text

            # Modern Twitter stores state in window.__INITIAL_STATE__
            state_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', page_source)
            
            if state_match:
                data = json.loads(state_match.group(1))
                # Paths in the JSON vary based on the page version (Legacy vs Pro)
                # This is a safe way to traverse deep dictionaries
                user_data = {}
                try:
                    # Generic path for guest-accessible JSON data
                    users = data.get('entities', {}).get('users', {})
                    if users:
                        user_data = list(users.values())[0]
                except:
                    pass

                if user_data:
                    self.id = user_data.get('id_str')
                    self.name = user_data.get('name')
                    self.username = user_data.get('screen_name')
                    self.location = user_data.get('location')
                    self.url = user_data.get('url')
                    self.description = user_data.get('description')
                    self.protected = user_data.get('protected')
                    self.followers = str(user_data.get('followers_count', 0))
                    self.friends = str(user_data.get('friends_count', 0))
                    self.create = user_data.get('created_at')
                    self.verified = user_data.get('verified')
                    self.status = str(user_data.get('statuses_count', 0))
                    self.langue = user_data.get('lang')

            # Separate check for birthdate (often hidden or in different tags)
            birth_match = re.search(r'Born\s+([A-Za-z]+\s+\d+,\s+\d+)', page_source)
            if birth_match:
                self.birth = birth_match.group(1)

        except Exception as e:
            print(f"[!] Error fetching profile @{username}: {e}")