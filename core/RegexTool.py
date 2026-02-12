import re

class RegexTool:
    def __init__(self, data):
        # Ensure data is a string to avoid attribute errors
        self.data = str(data)

    def get_emails(self):
        """Extracts all email addresses."""
        # Improved pattern to catch more complex email structures
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.emails = re.findall(pattern, self.data)
        return self.emails

    def get_phones_fr(self):
        """Extracts French phone numbers (standard and international)."""
        # Improved to catch spaces, dots, or dashes: 06 01 02... or +33 6...
        pattern = r'(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
        self.phones = re.findall(pattern, self.data)
        return self.phones

    def get_urls(self):
        """Extracts all HTTP/HTTPS URLs."""
        pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*'
        self.urls = re.findall(pattern, self.data)
        return self.urls

    def get_ipv4(self):
        """Extracts all IPv4 addresses from text."""
        # Removed ^ and $ so it can find IPs inside long strings
        pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        self.ipv4 = re.findall(pattern, self.data)
        return self.ipv4

    def get_ipv6(self):
        """Extracts all IPv6 addresses from text."""
        pattern = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
        # re.findall with many groups returns tuples; we want the full match
        matches = re.finditer(pattern, self.data)
        self.ipv6 = [m.group(0) for m in matches]
        return self.ipv6