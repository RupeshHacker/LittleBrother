import requests
import re
import json
import time
from urllib.parse import urljoin, quote

class Watcher:
    """
    Monitors Twitter and Instagram activity.
    Optimized for memory efficiency and cross-platform merging.
    """
    def __init__(self):
        self.tweet = {}
        self.medias = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def twitter_watcher(self, username):
        """Extracts recent tweet links and timestamps."""
        self.tweet = {}
        username = username.replace("@", "").strip()
        url_account = f"https://twitter.com/{username}"
        
        try:
            res = requests.get(url_account, headers=self.headers, timeout=10)
            if res.status_code == 200:
                # Optimized regex to find tweet IDs and timestamps in raw HTML
                # Note: Twitter often obfuscates this; regex is a 'best-effort' fallback
                matches = re.findall(r'href="/.*/status/(\d+)".*?data-time="(\d+)"', res.text)
                
                for tweet_id, timestamp in matches:
                    ts = int(timestamp)
                    self.tweet[ts] = {
                        "domain": "Twitter",
                        "tweet": f"{url_account}/status/{tweet_id}",
                        "date": time.ctime(ts),
                        "timestamp": ts
                    }
        except Exception as e:
            print(f"[!] Twitter Watcher Error: {e}")

    def instagram_watcher(self, username):
        """Extracts recent media, captions, and locations."""
        self.medias = {}
        username = username.replace("@", "").strip()
        url_account = f"https://www.instagram.com/{quote(username)}/"

        try:
            res = requests.get(url_account, headers=self.headers, timeout=10)
            if res.status_code != 200:
                return

            # Search for the modern __additionalDataLoaded or legacy _sharedData
            json_match = re.search(r'window\._sharedData\s*=\s*({.*?});', res.text)
            if not json_match:
                return

            data = json.loads(json_match.group(1))
            user_data = data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user')
            
            if not user_data or user_data.get('is_private'):
                return

            edges = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
            
            for edge in edges[:12]:  # Limit to 12 most recent
                node = edge.get('node', {})
                ts = node.get('taken_at_timestamp')
                if not ts: continue

                # Safe caption extraction using .get() and list checks
                captions = node.get('edge_media_to_caption', {}).get('edges', [])
                legende = captions[0]['node']['text'] if captions else ""

                self.medias[ts] = {
                    "domain": "Instagram",
                    "urlMedia": node.get('display_url'),
                    "type": "Video" if node.get('is_video') else "Photo",
                    "legende": legende,
                    "info": node.get('accessibility_caption', ""),
                    "location": node.get('location', {}).get('name') if node.get('location') else None,
                    "date": time.ctime(ts),
                    "timestamp": ts
                }
        except Exception as e:
            print(f"[!] Instagram Watcher Error: {e}")

    def get_unified_timeline(self):
        """Merges both dictionaries and sorts them by timestamp."""
        combined = {**self.tweet, **self.medias}
        # Returns a list of events sorted newest to oldest
        return sorted(combined.values(), key=lambda x: x['timestamp'], reverse=True)