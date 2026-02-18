import requests
import re
import json
import time
from urllib.parse import quote, urljoin

# Assuming these are your local helper modules
try:
    from core.getUrlGoogleSearch import getUrlGoogleSearch
    from lib.download import download
except ImportError:
    # Fallback or placeholder for standalone testing
    def getUrlGoogleSearch(x): return []
    def download(u, p, f): pass

class InstagramSearchTool:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def _get_json_data(self, page_source):
        """Extracts JSON blob from legacy Instagram sharedData script tags."""
        match = re.search(r'window\._sharedData\s*=\s*({.*?});', page_source)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None

    def _get_name_by_id(self, owner_id):
        """Fetches profile info via internal mobile API."""
        url = f"https://i.instagram.com/api/v1/users/{owner_id}/info/"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                data = res.json().get('user', {})
                return data.get('username'), data.get('full_name')
        except Exception:
            pass
        return None, None

    def _scrape_insta_explorer(self, page_source):
        """Generic scraper for Location and Tag pages."""
        results = {}
        values = self._get_json_data(page_source)
        if not values: return results

        try:
            # Try location data first, then fallback to hashtag data
            entry = values['entry_data']
            if 'LocationsPage' in entry:
                medias = entry['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
            else:
                medias = entry['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            
            # Use list slicing instead of while count to prevent crashes
            for edge in medias[:20]:
                node = edge['node']
                owner_id = node['owner']['id']
                
                # Fetching username by ID (Caution: Rate-limit intensive)
                username, name = self._get_name_by_id(owner_id)
                
                if username:
                    results[username] = {
                        "name": name,
                        "media": node.get('display_url'),
                        "id": owner_id,
                        "caption": (node['edge_media_to_caption']['edges'][0]['node']['text'] 
                                    if node['edge_media_to_caption']['edges'] else None)
                    }
        except (KeyError, IndexError):
            pass
        return results

    def get_info(self, username):
        """Fetches detailed profile information."""
        url = urljoin("https://instagram.com/", username.replace("http", "").strip("/"))
        res = requests.get(url, headers=self.headers, timeout=10)
        
        # Reset attributes
        attrs = ['id', 'profi_pic_hd', 'biography', 'username', 'name', 'private', 
                 'followers', 'friends', 'medias', 'email', 'address', 'phone']
        for attr in attrs: setattr(self, attr, None)

        if res.status_code == 200:
            data = self._get_json_data(res.text)
            if not data: return
            
            try:
                user = data['entry_data']['ProfilePage'][0]['graphql']['user']
                self.id = user.get('id')
                self.biography = user.get('biography')
                self.username = user.get('username')
                self.name = user.get('full_name')
                self.private = user.get('is_private')
                self.followers = user.get('edge_followed_by', {}).get('count')
                self.friends = user.get('edge_follow', {}).get('count')
                self.medias = user.get('edge_owner_to_timeline_media', {}).get('count')
                self.profi_pic_hd = user.get('profile_pic_url_hd')

                # Extract business info from ld+json if public
                ld_match = re.search(r'type="application/ld\+json">\s*({.*?})', res.text)
                if ld_match:
                    ld_data = json.loads(ld_match.group(1))
                    self.email = ld_data.get('email')
                    self.phone = ld_data.get('telephone')
                    self.address = ld_data.get('address', {}).get('addressLocality')
            except (KeyError, IndexError):
                pass

        # Backwards-compatible aliases expected by the project
    # Backwards-compatible aliases expected by the project
    def getInfo(self, username):
        return self.get_info(username)

    def getPicturesInfo(self, username):
        return self.get_pictures_info(username)

    def search_insta(self, query):
        """Searches Google for Instagram profiles."""
        google_url = f"https://www.google.com/search?q=site:instagram.com {quote(query)}"
        res = requests.get(google_url, headers=self.headers)
        urls = getUrlGoogleSearch(res.text)
        
        # Filter for profile URLs (avoiding posts '/p/')
        self.accounts = list(set(re.findall(r'instagram\.com/([^/p/][\w\.]+)', " ".join(urls))))

    def get_pictures_info(self, username):
        """Gets metadata for the last 11 posts."""
        results = {}
        url = urljoin("https://instagram.com/", username)
        res = requests.get(url, headers=self.headers, timeout=10)
        data = self._get_json_data(res.text)
        
        if not data: return results

        try:
            edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
            for i, edge in enumerate(edges[:11]):
                node = edge['node']
                ts = node.get('taken_at_timestamp')
                results[i] = {
                    "display": node.get('display_url'),
                    "type_media": "Video" if node.get('is_video') else "Photo",
                    "date": time.ctime(ts) if ts else None,
                    "info": node.get('accessibility_caption', ""),
                    "localisation": node.get('location', {}).get('name')
                }
        except (KeyError, IndexError):
            pass
        return results

    def downloadPictures(self, url, path, filename):
        """Convenience wrapper that uses the module-level `download` helper."""
        try:
            return download(url, path, filename)
        except Exception:
            return None


def instagramSearchTool():
    """Factory for backward compatibility: returns an InstagramSearchTool instance."""
    return InstagramSearchTool()
    