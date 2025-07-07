**Foxhound** is a reconnaissance automation tool designed to streamline offensive security assessments by automating port scanning, service enumeration, web fuzzing, and brute forcing.

---

## Features

- Fast port scanning with RustScan and Nmap
- Web fuzzing with FFUF
- FTP and SMB enumeration
- SSH and FTP brute force support
- Clean, colorized CLI output with summary reports
- Easy install and CLI usage via `foxhound` command

---

## Installation

Clone the repo and install dependencies with pip:

```bash
git clone https://github.com/LilithIsInHell/foxhound-recon.git
cd foxhound-recon
pip install -e .


Usage

Run recon on a target with:

foxhound -t 10.10.10.10

Common options:

  -t, --target       Target IP or domain (required)
  -o, --output       Output directory (default: timestamped)
  --brute-ssh        Enable SSH brute force
  --brute-ftp        Enable FTP brute force
  -u, --username     Username for brute force
  -w, --wordlist     Password wordlist for brute force
  --scan-only        Only perform port scan (skip enumeration)
  --version          Show version info


Contributing

Contributions and improvements are welcome! Feel free to open issues or submit pull requests.


Disclaimer

This tool is intended for authorized security testing only. Use responsibly.
```
