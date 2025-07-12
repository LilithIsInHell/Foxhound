import os
import re
import json
import requests
import hashlib
import base64
import mmh3

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from foxhound.utils import logger

DEFAULT_PORTS = [80, 443, 8080, 8000, 8443]
TIMEOUT = 5


def load_fingerprints():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fingerprints.json')
    with open(os.path.abspath(data_path), 'r') as f:
        return json.load(f)


def fetch_http_response(target, port):
    schemes = ['https://', 'http://'] if port in [443, 8443] else ['http://']
    for scheme in schemes:
        try:
            url = f"{scheme}{target}:{port}/"
            response = requests.get(url, timeout=TIMEOUT, verify=False, allow_redirects=True)
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

        # Future support: cert, js, path, etc.

    return confidence, details


def fingerprint_services(target, open_ports, output_dir):
    fingerprints = load_fingerprints()
    results = []

    for port in open_ports:
        if port not in DEFAULT_PORTS:
            continue

        logger.log(f"[*] Fingerprinting HTTP service on port {port}...")
        response = fetch_http_response(target, port)
        if not response:
            logger.log(f"[!] No response on port {port}. Skipping.", level="ERROR")
            continue

        scheme = 'https' if port in [443, 8443] else 'http'
        base_url = f"{scheme}://{target}:{port}"
        favicon_hash = get_favicon_hash(base_url)

        for fp in fingerprints:
            confidence, details = match_fingerprint(response, fp, favicon_hash)
            if confidence >= fp.get('confidence', 1.5):
                result = {
                    "port": port,
                    "fingerprint": fp['name'],
                    "confidence": confidence,
                    "details": details
                }
                results.append(result)
                logger.log(f"[+] Matched {fp['name']} on port {port} ({confidence})")

    # Save results to output dir
    output_path = os.path.join(output_dir, "fingerprint_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    return results
