# utils/logger.py
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level == "INFO":
        print(f"{Fore.CYAN}[{timestamp}] [*] {message}{Style.RESET_ALL}")
    elif level == "SUCCESS":
        print(f"{Fore.GREEN}[{timestamp}] [+] {message}{Style.RESET_ALL}")
    elif level == "ERROR":
        print(f"{Fore.RED}[{timestamp}] [!] {message}{Style.RESET_ALL}")
    else:
        print(f"[{timestamp}] {message}")

def banner():
    print(f"{Fore.MAGENTA}" + "=" * 70 + Style.RESET_ALL)
    print(f"{Fore.MAGENTA}{'FOXHOUND RECON STARTED':^70}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}" + "=" * 70 + Style.RESET_ALL)