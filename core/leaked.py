import requests
import json
import re
from urllib.parse import unquote

class Leaked:
    def __init__(self, hibp_api_key=None):
        self.api_key = hibp_api_key
        self.headers = {
            "User-Agent": "LittleBrother-OSINT-Scanner",
            "hibp-api-key": self.api_key
        }

    def hash_reverse(self, hash_value):
        """
        Attempts to reverse a hash using HashToolkit.
        Note: Many of these sites now require Cloudflare bypass or specific headers.
        """
        url = f"https://hashtoolkit.com/reverse-hash/?hash={hash_value}"
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if res.status_code == 200:
                # Optimized regex to find the decoded text
                passw = re.findall(r'/generate-hash/\?text=([^"]+)"', res.text)
                if passw:
                    # unquote handles URL-encoded characters in the password
                    return unquote(passw[0])
        except Exception as e:
            print(f"Error reversing hash: {e}")
        return None

    def check_email_breach(self, email):
        """
        Queries HaveIBeenPwned for email breaches.
        IMPORTANT: HIBP V3 requires an API Key.
        """
        if not self.api_key:
            return "Error: HIBP API Key required for V3. Visit https://haveibeenpwned.com/API/Key"

        # Updated to V3 API URL
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        
        try:
            # HIBP requires a specific 'truncateResponse' param or it might 404/403
            res = requests.get(url, headers=self.headers, params={'truncateResponse': 'false'}, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                # Using a list comprehension to build the breach list efficiently
                return [
                    {
                        'Title': d.get('Title'), 
                        'Domain': d.get('Domain'), 
                        'Date': d.get('BreachDate')
                    } for d in data
                ]
            elif res.status_code == 404:
                return []  # No breaches found
            elif res.status_code == 401:
                return "Error: Invalid API Key"
            elif res.status_code == 429:
                return "Error: Rate limit exceeded. Wait a few seconds."

        except Exception as e:
            return f"Connection Error: {e}"
        
        return None


    # Backwards-compatible alias expected by older modules
    def hash(self, hash_value):
        return self.hash_reverse(hash_value)


def leaked(hibp_api_key=None):
    """Factory for backward compatibility: returns a Leaked instance."""
    return Leaked(hibp_api_key=hibp_api_key)