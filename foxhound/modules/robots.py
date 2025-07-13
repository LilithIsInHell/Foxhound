# foxhound/modules/robots.py

import os
import requests
from urllib.parse import urljoin
from foxhound.utils import logger

TIMEOUT = 5

def fetch_robots_txt(target, port, output_dir):
    scheme = 'https' if port in [443, 8443] else 'http'
    base_url = f"{scheme}://{target}:{port}"
    robots_url = urljoin(base_url, "/robots.txt")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.6367.91 Safari/537.36"
    }

    try:
        response = requests.get(robots_url, timeout=TIMEOUT, verify=False, headers=headers)
        if response.status_code != 200 or "text/plain" not in response.headers.get("Content-Type", ""):
            logger.log(f"[!] No robots.txt on port {port}", level="DEBUG")
            return []

        lines = response.text.splitlines()
        entries = []

        logger.log(f"[+] Found robots.txt on port {port}")
        for line in lines:
            line = line.strip()
            if line.startswith(("Disallow:", "Allow:", "Sitemap:")):
                logger.log(f"    └─ {line}")
                entries.append(line)

        # Save to output
        output_path = os.path.join(output_dir, f"robots_{port}.txt")
        with open(output_path, "w") as f:
            f.write(response.text)

        return entries

    except requests.RequestException as e:
        logger.log(f"[!] Failed to fetch robots.txt from {robots_url} → {e}", level="DEBUG")
        return []
