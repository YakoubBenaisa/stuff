"""
Ethical SQL Injection Scanner - For Educational Use Only
"""
import requests
import colorama
import datetime
import time
import socket
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

colorama.init(autoreset=True)

# Ethical Configuration
CONSENT_WARNING = """
[!] IMPORTANT LEGAL AND ETHICAL NOTICE [!]
This tool should only be used:
1. On websites you own
2. With explicit written permission from the website owner
3. In compliance with all applicable laws

By using this tool, you agree to:
- Not engage in unauthorized security testing
- Respect robots.txt and website terms of service
- Immediately disclose findings to the website owner
- Not use this tool for malicious purposes

Type 'AGREE' to confirm you have proper authorization: """

class Scanner:
    def __init__(self):
        self.headers = {'User-Agent': 'EthicalSecurityScanner/1.0',
                        'X-Scanner-ID': str(hash(socket.gethostname()))}
        self.errors = [
            # Reduced fingerprinting signatures to minimize detection
            'sql syntax',
            'unclosed quotation',
            'syntax error'
        ]
        self.excluded_domains = [
            '.gov', '.edu', '.mil', 
            'localhost', '127.0.0.1'
        ]
        self.rate_limit = 1  # Seconds between requests
        self.timeout = 3     # Request timeout in seconds

    def validate_ethics(self):
        """Ensure user consent and authorization"""
        consent = input(CONSENT_WARNING).strip().upper()
        if consent != 'AGREE':
            print("Aborting scan due to lack of authorization")
            exit()

    def is_authorized_domain(self, url):
        """Check against excluded domains"""
        parsed = urlparse(url)
        for domain in self.excluded_domains:
            if domain in parsed.netloc:
                print(f"Scanning prohibited for {parsed.netloc}")
                return False
        return True

    def get_links(self, base_url):
        """Collect links with proper domain validation"""
        if not self.is_authorized_domain(base_url):
            return []

        try:
            resp = requests.get(base_url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(resp.text, 'html.parser')
            return [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)
                    if '.php' in a['href'] and self.is_authorized_domain(a['href'])]
        except Exception as e:
            print(f"Error collecting links: {str(e)}")
            return []

    def test_vulnerability(self, url):
        """Limited test with safe payloads"""
        try:
            test_url = f"{url}?ed=1'"
            resp = requests.get(test_url, headers=self.headers, timeout=self.timeout)
            content = resp.text.lower()
            return any(error in content for error in self.errors)
        except:
            return False

    def scan(self, base_url):
        """Conduct ethical scan with safeguards"""
        self.validate_ethics()
        
        print(f"\n{colorama.Fore.CYAN}[•] Starting ethical scan of {base_url}")
        print(f"{colorama.Fore.YELLOW}[!] Rate limited to {self.rate_limit}s/request")
        
        links = self.get_links(base_url)
        findings = []

        for idx, url in enumerate(links, 1):
            print(f"{colorama.Fore.WHITE}[{idx}/{len(links)}] Testing {url}")
            
            if self.test_vulnerability(url):
                finding = f"{colorama.Fore.RED}[!] Potential vulnerability found: {url}"
                print(finding)
                findings.append(finding)
                # Immediate disclosure recommendation
                print(f"{colorama.Fore.YELLOW}[!] Report to: security@{urlparse(url).netloc}")
            
            time.sleep(self.rate_limit)

        print(f"\n{colorama.Fore.GREEN}[•] Scan complete")
        print(f"{colorama.Fore.YELLOW}[!] Found {len(findings)} potential issues")
        print(f"{colorama.Fore.CYAN}[•] Ethical next steps:")
        print("- Immediately notify website owner")
        "- Do not attempt exploitation\n"
        "- Document findings responsibly"

        return findings

if __name__ == '__main__':
    scanner = canner()
    target_url = input("Enter authorized target URL: ").strip()
    
    try:
        results = scanner.scan(target_url)
        with open('ethical_report.txt', 'w') as f:
            f.write("\n".join(results))
    except KeyboardInterrupt
        print("\nScan aborted by user")