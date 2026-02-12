import re
from urllib.parse import unquote

def get_url_google_search(content):
    """
    Extracts, decodes, and filters Google search result URLs.
    """
    # 1. Extract all potential URLs using regex
    # Added 'r' for raw string and simplified the pattern
    raw_urls = re.findall(r'url\?q=(.*?)&', content)
    
    # 2. Define exclusion keywords for filtering
    excludes = {"googleusercontent", "/settings/ads", "/policies/faq"}
    
    # 3. Process the list in a single pass (List Comprehension)
    # unquote() replaces your entire encodeDic loop
    return [
        unquote(url) for url in raw_urls 
        if not any(x in unquote(url) for x in excludes)
    ]

# --- Example Usage ---
if __name__ == "__main__":
    sample_data = "Example: url?q=https://example.com/%21%23%24&sa=U... url?q=https://googleusercontent.com/test&sa=U"
    results = get_url_google_search(sample_data)
    
    for link in results:
        print(f"Found: {link}")