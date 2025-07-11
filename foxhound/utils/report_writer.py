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


   
