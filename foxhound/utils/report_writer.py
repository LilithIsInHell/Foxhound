# utils/report_writer.py
import os
from datetime import datetime

def generate_report(target, output_dir):
    report_path = os.path.join(output_dir, "report.md")

    with open(report_path, 'w') as report:
        report.write(f"#FOXHOUND-RECON REPORT\n\n")
        report.write(f"**Target:** `{target}`  ")
        report.write(f"**Date:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n")

        report.write("##Table of Contents\n")
        report.write("- [Port Scan Results](#-port-scan-results)\n")
        report.write("- [Web Fuzzing](#-web-fuzzing)\n")
        report.write("- [SMB Enumeration](#-smb-enumeration)\n")
        report.write("- [FTP Enumeration](#-ftp-enumeration)\n")
        report.write("- [Brute Force Attempts](#-brute-force-attempts)\n\n")

        report.write("##Port Scan Results\n")
        nmap_file = os.path.join(output_dir, "nmap_scan.txt")
        if os.path.exists(nmap_file):
            with open(nmap_file, 'r') as nmap:
                report.write("\n```plaintext\n")
                report.write(nmap.read())
                report.write("\n```\n")
        else:
            report.write("_Nmap results not found._\n")

        report.write("\n##Web Fuzzing\n")
        web_fuzz_summary = os.path.join(output_dir, "web_fuzz_summary.txt")
        if os.path.exists(web_fuzz_summary):
            with open(web_fuzz_summary, 'r') as wf:
                report.write("\n```plaintext\n")
                report.write(wf.read())
                report.write("\n```\n")
        else:
            report.write("_No web fuzzing results found._\n")

        report.write("\n##SMB Enumeration\n")
        smb_file = os.path.join(output_dir, "smb_enum.txt")
        if os.path.exists(smb_file):
            with open(smb_file, 'r') as smb:
                report.write("\n```plaintext\n")
                report.write(smb.read())
                report.write("\n```\n")
        else:
            report.write("_No SMB enumeration results found._\n")

        report.write("\n##FTP Enumeration\n")
        ftp_file = os.path.join(output_dir, "ftp_enum.txt")
        if os.path.exists(ftp_file):
            with open(ftp_file, 'r') as ftp:
                report.write("\n```plaintext\n")
                report.write(ftp.read())
                report.write("\n```\n")
        else:
            report.write("_No FTP enumeration results found._\n")

        report.write("\n##Brute Force Attempts\n")
        ssh_brute = os.path.join(output_dir, "ssh_brute.txt")
        if os.path.exists(ssh_brute):
            report.write("\n###SSH Brute Force\n")
            with open(ssh_brute, 'r') as ssh:
                report.write("\n```plaintext\n")
                report.write(ssh.read())
                report.write("\n```\n")
        else:
            report.write("_No SSH brute force results found._\n")

        ftp_brute = os.path.join(output_dir, "ftp_brute.txt")
        if os.path.exists(ftp_brute):
            report.write("\n###FTP Brute Force\n")
            with open(ftp_brute, 'r') as ftp:
                report.write("\n```plaintext\n")
                report.write(ftp.read())
                report.write("\n```\n")
        else:
            report.write("_No FTP brute force results found._\n")

   
