import os
import re
import json
import socket
import requests
from colorama import init, Fore

# Initialize colors
init(autoreset=True)

# UI Icons
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
F = f"[{Fore.GREEN}+{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"
I = f"[{Fore.BLUE}I{Fore.RESET}]"

class MailAnalyzer:
    def __init__(self):
        self.headers = {"User-Agent": "Kali-OSINT-Scanner"}

    def get_ip_details(self, ip):
        """Combined ISP and Geo-location lookup using a stable API."""
        try:
            # ip-api.com is fast and doesn't require a key for basic usage
            res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = res.json()
            if data.get("status") == "success":
                return {
                    "isp": data.get("isp", "Unknown"),
                    "loc": f"{data.get('country')}, {data.get('regionName')}, {data.get('city')}",
                    "org": data.get("org", "Unknown")
                }
        except:
            pass
        return {"isp": "Unknown", "loc": "Unknown", "org": "Unknown"}

    def is_public_ip(self, ip):
        """Filters out local/private IPs that won't have Geo-data."""
        # Regex for private IP ranges (10.x, 172.16.x, 192.168.x, 127.x)
        private_pattern = re.compile(
            r'^(10\.|127\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|192\.168\.)'
        )
        return not private_pattern.match(ip)

    def analyze(self):
        file_path = input(f"{Q} Chemin de l'entête (Header path): ").strip()
        
        if not os.path.exists(file_path):
            print(f"\n{W} Fichier introuvable.")
            return

        print(f"\n{S} Analyse des entêtes en cours...\n")

        # Use 'with' to ensure file closes automatically
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                # Identify Sender
                if line.startswith("From: "):
                    print(f"{I} Expéditeur: {line.replace('From: ', '')}")
                
                # Identify Routing IPs
                if 'Received:' in line:
                    ip_matches = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                    for ip in ip_matches:
                        if self.is_public_ip(ip):
                            details = self.get_ip_details(ip)
                            
                            # Resolve Domain
                            try:
                                domain = socket.gethostbyaddr(ip)[0]
                            except:
                                domain = "No PTR record"

                            print(f"\n[{Fore.CYAN}{ip}{Fore.RESET}]")
                            print(f" ├ Domain: {domain}")
                            print(f" ├ ISP:    {details['isp']}")
                            print(f" └ Loc:    {details['loc']}")

if __name__ == "__main__":
    analyzer = MailAnalyzer()
    analyzer.analyze()


def mailToIP():
    """Backward-compatible wrapper: runs the mail header analyzer."""
    analyzer = MailAnalyzer()
    return analyzer.analyze()