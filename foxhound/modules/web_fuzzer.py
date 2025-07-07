# modules/web_fuzzer.py
import subprocess
import os
from utils import logger

def fuzz_web(target, output_dir):
    output_file = os.path.join(output_dir, "web_fuzz.txt")
    logger.log(f"[*] Starting web fuzzing on {target}")

    # Define target URL
    url = f"http://{target}"

    # FFUF basic fuzzing command 
    cmd = [
        "ffuf",
        "-w", "/usr/share/wordlists/dirb/common.txt",
        "-u", f"{url}/FUZZ",
        "-o", output_file,
        "-of", "md",
        "-s"
    ]

    try:
        subprocess.run(cmd, check=True)
        logger.log(f"[+] Web fuzzing complete. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logger.log("[!] FFUF failed to execute.", level="ERROR")
        logger.log(str(e), level="ERROR")
    except FileNotFoundError:
        logger.log("[!] FFUF not found. Make sure it is installed and in your PATH.", level="ERROR")
