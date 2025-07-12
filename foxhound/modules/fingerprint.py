import os
import re
import json
import requests
import base64
import mmh3

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from foxhound.utils import logger

TIMEOUT = 5


def load_fingerprints():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fingerprints.json')
    with open(os.path.abspath(data_path), 'r') as f:
        return json.load(f)


def fetch_http_response(target, port):
    schemes = ['https://', 'http://'] if port in [443, 8443] else ['http://']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.6367.91 Safari/537.36"
    }

    for scheme in schemes:
        url = f"{scheme}{target}:{port}/"
        try:
            response = requests.get(url, timeout=TIMEOUT, verify=False, allow_redirects=True, headers=headers)
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type == "" or any(x in content_type for x in ["text", "html", "xml", "json"]):
                return response
        except requests.RequestException:
            continue
    return None


def get_favicon_hash(base_url):
    try:
        favicon_url = urljoin(base_url, "/favicon.ico")
        response = requests.get(favicon_url, timeout=TIMEOUT, verify=False)
        if response.status_code == 200:
            favicon_data = base64.b64encode(response.content)
            return str(mmh3.hash(favicon_data))
    except requests.RequestException:
        pass
    return None


def extract_title(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        return soup.title.string.strip() if soup.title else ""
    except Exception:
        return ""


def match_fingerprint(response, fingerprint, favicon_hash=None):
    confidence = 0
    details = []

    body = response.text
    headers = dict(response.headers)
    title = extract_title(body)

    for match in fingerprint.get("matches", []):
        part = match.get("part")
        pattern = match.get("pattern", "")
        weight = match.get("confidence", 1.0)

        if part == "headers":
            for header, value in headers.items():
                target_str = f"{header}: {value}"
                if re.search(pattern, target_str, re.IGNORECASE):
                    confidence += weight
                    details.append(f"[Header] {header}: matched '{pattern}' (+{weight})")

        elif part == "body":
            if re.search(pattern, body, re.IGNORECASE):
                confidence += weight
                details.append(f"[Body] matched '{pattern}' (+{weight})")

        elif part == "title":
            if re.search(pattern, title, re.IGNORECASE):
                confidence += weight
                details.append(f"[Title] matched '{pattern}' (+{weight})")

        elif part == "favicon_hash":
            if favicon_hash and pattern == favicon_hash:
                confidence += weight
                details.append(f"[Favicon] hash matched '{pattern}' (+{weight})")

    return confidence, details


def fingerprint_services(target, open_ports, output_dir):
    fingerprints = load_fingerprints()
    results = []
    favicon_cache = {}

    for port in open_ports:
        logger.log(f"[*] Probing port {port} for HTTP service...")

        scheme = 'https' if port in [443, 8443] else 'http'
        base_url = f"{scheme}://{target}:{port}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.6367.91 Safari/537.36"
        }

        for fp in fingerprints:
            paths = fp.get("paths", ["/"])  # Default to root if no paths

            for path in paths:
                full_url = f"{base_url}{path}"
                try:
                    response = requests.get(full_url, timeout=TIMEOUT, verify=False, allow_redirects=True, headers=headers)
                    content_type = response.headers.get("Content-Type", "").lower()

                    if content_type == "" or any(x in content_type for x in ["text", "html", "xml", "json"]):
                        if port not in favicon_cache:
                            favicon_cache[port] = get_favicon_hash(base_url)
                        favicon_hash = favicon_cache[port]

                        confidence, details = match_fingerprint(response, fp, favicon_hash)
                        if confidence >= fp.get('confidence', 1.5):
                            result = {
                                "port": port,
                                "path": path,
                                "fingerprint": fp['name'],
                                "confidence": confidence,
                                "details": details
                            }
                            results.append(result)

                            logger.log(f"[+] Matched {fp['name']} on {port}{path} ({confidence})")
                            for i, d in enumerate(details):
                                branch = "└─" if i == len(details) - 1 else "├─"
                                logger.log(f"    {branch} {d}")
                            break  # Stop after first good match
                except requests.RequestException:
                    continue

    output_path = os.path.join(output_dir, "fingerprint_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    return results
