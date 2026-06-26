import os
import ftplib
from pathlib import Path

FTP_HOST = "94.73.150.7"
FTP_USER = "u2756116@kafetakip.com"
FTP_PASS = "SerkanKose19."

FILES_TO_UPLOAD = [
    "scraper.py",
    "smart_scraper.py",
    "telegram_notifier.py",
    "run.sh",
    "companies.json",
    "requirements.txt",
    ".env"
]

OUTPUT_FILES = [
    "latest.json",
    "sent_jobs.json",
    "report.html"
]

def upload():
    try:
        print("Connecting to FTP...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected!")
        
        for file in FILES_TO_UPLOAD:
            if os.path.exists(file):
                print(f"Uploading {file}...")
                with open(file, 'rb') as f:
                    ftp.storbinary(f'STOR {file}', f)
                    
        # upload output files to output dir
        try:
            ftp.mkd('output')
        except:
            pass # might already exist
            
        for file in OUTPUT_FILES:
            local_path = os.path.join("output", file)
            if os.path.exists(local_path):
                print(f"Uploading output/{file}...")
                with open(local_path, 'rb') as f:
                    ftp.storbinary(f'STOR output/{file}', f)
                    
        # upload report as index.html
        local_report = os.path.join("output", "report.html")
        if os.path.exists(local_report):
            print("Uploading report.html as index.html...")
            with open(local_report, 'rb') as f:
                ftp.storbinary('STOR index.html', f)
                
        # chmod run.sh to executable if possible, ftp doesn't always support it natively via SITE CHMOD but we can try
        try:
            ftp.sendcmd('SITE CHMOD 755 run.sh')
        except:
            pass
            
        ftp.quit()
        print("All files uploaded successfully!")
    except Exception as e:
        print(f"FTP Error: {e}")

if __name__ == "__main__":
    upload()
