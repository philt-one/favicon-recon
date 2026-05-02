# Favicon Recon

A powerful reconnaissance tool for extracting favicon hashes from websites and generating search queries for cybersecurity intelligence platforms like Shodan and FOFA.

Inspiration for the project came from [Mejbaur Bahar Fagun
](https://fagun18.medium.com/about) in his [article](https://fagun18.medium.com/using-favicon-hashes-for-osint-reconnaissanc-cefcb8c4ddca).

## Overview

This tool retrieves favicons from target websites, calculates their MurmurHash3 (mmh3) hashes, and generates ready-to-use queries for popular threat intelligence platforms. Favicon hashing is a valuable technique for identifying web infrastructure, tracking technology stacks, and discovering related assets across the internet.

## Features

- **Single URL & Bulk Processing**: Target individual websites or process multiple URLs from a file
- **Smart Favicon Detection**: Automatically parses HTML to find favicon locations, with fallback to default paths
- **Concurrent Processing**: Multi-threaded execution for efficient bulk scanning
- **Multiple Output Formats**: Console output and JSON export for integration with other tools
- **Platform Queries**: Generates search queries for Shodan and FOFA platforms
- **Error Handling**: Robust error handling with detailed status reporting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/philt-one/favicon-recon
cd favicon-recon
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies

- `mmh3` - MurmurHash3 implementation for favicon hashing
- `requests` - HTTP client for web requests
- `beautifulsoup4` - HTML parsing for favicon link detection

## Usage

### Single URL Mode

```bash
python favicon_recon.py -u https://example.com
```

### Bulk Processing Mode

Create a text file with one URL per line (`targets.txt`):
```
https://example.com
https://test-site.org
https://demo-app.net
```

Then run:
```bash
python favicon_recon.py -i targets.txt
```

### Advanced Options

```bash
python favicon_recon.py -i targets.txt -o results.json -t 10
```

- `-o, --output`: Save results to JSON file
- `-t, --threads`: Number of concurrent threads (default: 5)

## Output

### Console Output
```
[*] Target: https://example.com
[+] Favicon URL: https://example.com/favicon.ico
[>] Hash (mmh3): 123456789
    Shodan: http.favicon.hash:123456789
    FOFA:   icon_hash="123456789"
```

### JSON Output
```json
[
    {
        "target": "https://example.com",
        "favicon_url": "https://example.com/favicon.ico",
        "hash": 123456789,
        "shodan_query": "http.favicon.hash:123456789",
        "fofa_query": "icon_hash=\"123456789\"",
        "error": null
    }
]
```

## Use Cases

- **Asset Discovery**: Find related web infrastructure using shared favicons
- **Technology Fingerprinting**: Identify web frameworks, CMS platforms, and custom applications
- **Security Research**: Track malicious infrastructure across multiple domains
- **Competitive Analysis**: Discover technology stacks used by competitors
- **Bug Bounty Hunting**: Expand attack surface by finding related assets

## How It Works

1. **Favicon Detection**: The tool parses the target website's HTML to find favicon link tags (`<link rel="icon">`)
2. **Fallback Mechanism**: If no favicon is found in HTML, it checks the default `/favicon.ico` location
3. **Hash Calculation**: Downloads the favicon and calculates its mmh3 hash after base64 encoding
4. **Query Generation**: Creates platform-specific search queries for Shodan and FOFA

## Security Considerations

- The tool disables SSL verification by default for compatibility with various sites
- User-Agent headers are set to mimic legitimate browser traffic
- Timeout values prevent hanging on unresponsive targets
- All network requests include appropriate error handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for legitimate security research and authorized testing purposes only. Users are responsible for ensuring they have proper authorization before scanning any targets.
