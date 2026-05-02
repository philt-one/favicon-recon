import mmh3
import requests
import codecs
import argparse
import json
import concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3
import sys

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def find_favicon_url(base_url):
    """Parses the target URL's HTML to find the true favicon location."""
    if not base_url.startswith('http'):
        base_url = 'http://' + base_url
        
    try:
        response = requests.get(base_url, headers=HEADERS, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the icon link tag
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        
        if icon_link and icon_link.get('href'):
            # Resolve relative URLs (e.g., '/assets/favicon.png') to absolute URLs
            return urljoin(base_url, icon_link.get('href'))
            
    except Exception:
        pass # Fallback to default if connection fails or no tag is found
        
    # Fallback to the default location
    parsed_url = urlparse(base_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

def process_target(url):
    """Fetches the favicon and calculates the mmh3 hash."""
    result = {
        "target": url,
        "favicon_url": None,
        "hash": None,
        "shodan_query": None,
        "fofa_query": None,
        "error": None
    }
    
    try:
        favicon_url = find_favicon_url(url)
        result["favicon_url"] = favicon_url
        
        response = requests.get(favicon_url, headers=HEADERS, verify=False, timeout=10)
        
        if response.status_code == 200:
            favicon_base64 = codecs.encode(response.content, "base64")
            favicon_hash = mmh3.hash(favicon_base64)
            
            result["hash"] = favicon_hash
            result["shodan_query"] = f"http.favicon.hash:{favicon_hash}"
            result["fofa_query"] = f'icon_hash="{favicon_hash}"'
        else:
            result["error"] = f"HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
        
    return result

def print_result(res):
    """Prints a single result to the console."""
    print(f"\n[*] Target: {res['target']}")
    if res['error']:
        print(f"[-] Failed: {res['error']}")
    else:
        print(f"[+] Favicon URL: {res['favicon_url']}")
        print(f"[>] Hash (mmh3): {res['hash']}")
        print(f"    Shodan: {res['shodan_query']}")
        print(f"    FOFA:   {res['fofa_query']}")

def main():
    parser = argparse.ArgumentParser(description="Favicon Hash Reconnaissance Tool v1.0")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="Target a single URL")
    group.add_argument("-i", "--input", help="Target a text file containing multiple URLs")
    parser.add_argument("-o", "--output", help="Save output to a JSON file")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of concurrent threads (default: 5)")
    
    args = parser.parse_args()
    results = []

    # Single URL mode
    if args.url:
        res = process_target(args.url)
        print_result(res)
        results.append(res)
        
    # Bulk input mode
    elif args.input:
        try:
            with open(args.input, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
                
            print(f"[*] Loaded {len(urls)} targets. Starting scan with {args.threads} threads...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
                # Map the process_target function to the URLs
                future_to_url = {executor.submit(process_target, url): url for url in urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    res = future.result()
                    print_result(res)
                    results.append(res)
                    
        except FileNotFoundError:
            print(f"[-] Error: Could not find file '{args.input}'")
            sys.exit(1)

    # Save to JSON if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"\n[+] Results successfully saved to {args.output}")

if __name__ == "__main__":
    main()