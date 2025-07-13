# main.py
import argparse
import os
import time
from datetime import datetime
from foxhound.modules import scanner, web_fuzzer, smb_enum, ftp_enum
from foxhound.utils import logger, report_writer
from foxhound.utils.dependency_check import check_dependencies
from colorama import Fore, Style
from foxhound.modules import fingerprint
from foxhound.modules import robots

def print_banner():
    banner = r'''

░        ░░░      ░░░  ░░░░  ░░  ░░░░  ░░░      ░░░  ░░░░  ░░   ░░░  ░░       ░░
▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒    ▒▒  ▒▒  ▒▒▒▒  ▒
▓      ▓▓▓▓  ▓▓▓▓  ▓▓▓▓    ▓▓▓▓        ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓  ▓  ▓  ▓▓  ▓▓▓▓  ▓
█  ████████  ████  ███  ██  ███  ████  ██  ████  ██  ████  ██  ██    ██  ████  █
█  █████████      ███  ████  ██  ████  ███      ████      ███  ███   ██       ██
                                                                                
                       Pentesting Recon Automation Tool
'''
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="Foxhound - Pentesting Recon Automation Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-o", "--output", help="Output directory (default: timestamped)")
    parser.add_argument("--scan-only", action="store_true", help="Only perform port scan")
    parser.add_argument("--version", action="version", version="Foxhound v1.0")
    args = parser.parse_args()

    print_banner()
    logger.banner()
    logger.log(f"[*] Starting recon on target: {args.target}")

    # Dependency check
    if not check_dependencies():
        return

    # Handle output directory
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join("output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()
    open_ports = scanner.scan_target(args.target, output_dir)

    # Fingerprint web services automatically
    fingerprint_results = fingerprint.fingerprint_services(args.target, open_ports, output_dir)
    
    robots_results = {}

    for port in open_ports:
        if port in [80, 443, 8080, 8443, 8000, 50000]:
            entries = robots.fetch_robots_txt(args.target, port, output_dir)
            if entries:
                robots_results[port] = entries

    ran_web = ran_ftp_enum = ran_smb = False

    if args.scan_only:
        logger.log("[*] Scan-only mode enabled. Skipping enumeration.")
        report_writer.generate_report(args.target, output_dir)
    else:
        if 80 in open_ports or 443 in open_ports:
            web_fuzzer.fuzz_web(args.target, output_dir)
            ran_web = True

        if 21 in open_ports:
            ftp_enum.enum_ftp(args.target, output_dir)
            ran_ftp_enum = True

        if 445 in open_ports:
            smb_enum.enum_smb(args.target, output_dir)
            ran_smb = True

        report_writer.generate_report(args.target, output_dir)

    duration = time.time() - start_time
    minutes, seconds = divmod(int(duration), 60)
    logger.log(f"[*] Recon complete in {minutes} minutes, {seconds} seconds.")

   # Final scan summary with color
    logger.log("\n" + Fore.CYAN + Style.BRIGHT + "[+] Scan Summary" + Style.RESET_ALL)
    logger.log(Fore.YELLOW + "- Open Ports: " + ", ".join(map(str, open_ports)) + Style.RESET_ALL)
    logger.log(Fore.YELLOW + "- Web Fuzzing: " + (Fore.GREEN + "✔" if ran_web else Fore.RED + "✘") + Style.RESET_ALL)
    logger.log(Fore.YELLOW + "- FTP Enum: " + (Fore.GREEN + "✔" if ran_ftp_enum else Fore.RED + "✘") + Style.RESET_ALL)
    logger.log(Fore.YELLOW + "- SMB Enum: " + (Fore.GREEN + "✔" if ran_smb else Fore.RED + "✘") + Style.RESET_ALL)
    if fingerprint_results:
        logger.log(Fore.YELLOW + "- Fingerprints:" + Style.RESET_ALL)
        for result in fingerprint_results:
            logger.log(Fore.GREEN + f"  - Port {result['port']}: {result['fingerprint']} ({result['confidence']}%)" + Style.RESET_ALL)
    else:
        logger.log(Fore.YELLOW + "- Fingerprints: " + Fore.RED + "✘ No matches" + Style.RESET_ALL)
    if robots_results:
        logger.log(Fore.YELLOW + "- Robots.txt Findings:" + Style.RESET_ALL)
        for port, entries in robots_results.items():
            logger.log(Fore.GREEN + f"  - Port {port}:" + Style.RESET_ALL)
            for entry in entries:
                logger.log("    └─ " + entry)
    else:
        logger.log(Fore.YELLOW + "- Robots.txt Findings: " + Fore.RED + "✘ None found" + Style.RESET_ALL)

    logger.log(Fore.YELLOW + f"- Report Path: {os.path.join(output_dir, 'report.md')}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
