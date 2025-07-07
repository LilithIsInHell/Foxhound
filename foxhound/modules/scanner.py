# modules/scanner.py
import subprocess
import os
import threading
import time
import itertools
import sys

def spinner(msg, stop_event):
    spinner_cycle = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f"\r{msg} " + next(spinner_cycle))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(msg) + 2) + "\r")  # Clear line

def scan_target(target, output_dir):
    output_file = os.path.join(output_dir, "nmap_scan.txt")
    scan_cmd = [
        "rustscan", "-a", target, "--ulimit", "5000",
        "--", "-sC", "-sV", "-oN", output_file
    ]

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(f"[+] Scanning {target}", stop_spinner))
    spinner_thread.start()

    try:
        result = subprocess.run(scan_cmd, capture_output=True, text=True)
    finally:
        stop_spinner.set()
        spinner_thread.join()

    if result.returncode != 0:
        print("[!] Rustscan failed to execute. Check installation.")
        print(result.stderr)
        return []

    # Parse open ports
    open_ports = []
    try:
        with open(output_file, 'r') as file:
            for line in file:
                if "/tcp" in line and "open" in line:
                    port = int(line.split("/")[0])
                    open_ports.append(port)
    except Exception as e:
        print(f"[!] Error parsing scan output: {e}")

    print(f"[*] Open ports found: {open_ports}")
    return open_ports
