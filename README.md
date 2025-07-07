![image](https://github.com/user-attachments/assets/b71c8ac0-a7a4-4256-8c0e-fe9b44dad3b5)

**Foxhound** is a modular reconnaissance automation tool designed to streamline offensive security assessments by automating port scanning, service enumeration, web fuzzing, and brute forcing.

## Features

- Port scanning with RustScan and Nmap
- Web fuzzing with FFUF
- FTP and SMB enumeration
- SSH and FTP brute force support
- Clean, colorized CLI output with summary reports
- Easy install and CLI usage via `foxhound` command

## Installation

### Requirements

- Python 3.8+
- Installed tools: `rustscan`, `nmap`, `ffuf`, `hydra`

Clone the repo and install dependencies with pip:

```bash
git clone https://github.com/LilithIsInHell/Foxhound.git
cd Foxhound
pip install -e .
```

## Usage

Run recon on a target with:

```bash
foxhound -t 10.10.10.10
```

## Arguments:

`-t, --target` Target IP or domain (required)

`-o, --output` Output directory (default: timestamped)

`--brute-ssh` Enable SSH brute force

`--brute-ftp` Enable FTP brute force

`-u, --username` Username for brute force

`-w, --wordlist` Password wordlist for brute force

`--scan-only` Only perform port scan (skip enumeration)

`--version` Show version info

## Contributing

Contributions and improvements are welcome! Feel free to open issues or submit pull requests.

## Disclaimer

This tool is intended for authorized security testing only. Use responsibly.
