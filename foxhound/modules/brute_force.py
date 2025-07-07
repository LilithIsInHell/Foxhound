# modules/brute_force.py
import subprocess
import os
from utils import logger

def brute_force_ssh(target, output_dir, username, wordlist):
    output_file = os.path.join(output_dir, "ssh_brute.txt")
    logger.log(f"[*] Starting SSH brute force on {target} with username '{username}'")

    cmd = [
        "hydra",
        "-l", username,
        "-P", wordlist,
        target,
        "ssh",
        "-o", output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        logger.log(f"[+] SSH brute force complete. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logger.log("[!] Hydra SSH brute force failed.", level="ERROR")
        logger.log(str(e), level="ERROR")
    except FileNotFoundError:
        logger.log("[!] Hydra not found. Make sure it is installed and in your PATH.", level="ERROR")

def brute_force_ftp(target, output_dir, username, wordlist):
    output_file = os.path.join(output_dir, "ftp_brute.txt")
    logger.log(f"[*] Starting FTP brute force on {target} with username '{username}'")

    cmd = [
        "hydra",
        "-l", username,
        "-P", wordlist,
        target,
        "ftp",
        "-o", output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        logger.log(f"[+] FTP brute force complete. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logger.log("[!] Hydra FTP brute force failed.", level="ERROR")
        logger.log(str(e), level="ERROR")
    except FileNotFoundError:
        logger.log("[!] Hydra not found. Make sure it is installed and in your PATH.", level="ERROR")
