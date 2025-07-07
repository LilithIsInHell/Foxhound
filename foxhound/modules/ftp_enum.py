# modules/ftp_enum.py
import ftplib
import os
from foxhound.utils import logger

def enum_ftp(target, output_dir):
    output_file = os.path.join(output_dir, "ftp_enum.txt")
    logger.log(f"[*] Attempting anonymous FTP login on {target}")

    try:
        ftp = ftplib.FTP(target)
        ftp.login()
        logger.log(f"[+] Anonymous FTP login successful on {target}")

        with open(output_file, 'w') as f:
            f.write(f"Anonymous FTP Login to {target} successful\n")
            f.write("Directory listing:\n")
            files = ftp.nlst()
            for file in files:
                f.write(f" - {file}\n")

        ftp.quit()
        logger.log(f"[+] FTP enumeration complete. Output saved to {output_file}")

    except ftplib.error_perm as e:
        logger.log("[!] Anonymous FTP login failed.", level="ERROR")
        logger.log(str(e), level="ERROR")
    except Exception as e:
        logger.log("[!] FTP connection error.", level="ERROR")
        logger.log(str(e), level="ERROR")
