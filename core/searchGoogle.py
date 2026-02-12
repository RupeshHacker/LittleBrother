import re
from urllib.parse import unquote

def search_google(request_main=None, request_secondary=None):
    """
    Parses Google search responses to extract and decode clean URLs.
    """
    # Define keywords to filter out (Google internal pages)
    excludes = {"googleusercontent", "/settings/ads", "/policies/faq"}

    def process_content(response, prefix="[+]"):
        if not response:
            return
        
        content = response.text
        # Extract the 'q' parameter from Google's redirect URLs
        raw_urls = re.findall(r'url\?q=(.*?)&', content)
        
        for url in raw_urls:
            # unquote() handles all %XX characters automatically
            decoded_url = unquote(url)
            
            # Filter and display
            if not any(x in decoded_url for x in excludes):
                print(f"{prefix} Possible connection: {decoded_url}")

    # Process both requests if they exist
    if request_secondary:
        process_content(request_secondary, prefix="[++]")
    
    if request_main:
        process_content(request_main, prefix="[+]")