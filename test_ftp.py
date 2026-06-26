import ftplib
try:
    ftp = ftplib.FTP('94.73.150.7')
    ftp.login('u2756116@kafetakip.com', 'SerkanKose19.')
    print("Login successful!")
    print("Directory listing:")
    ftp.dir()
    ftp.quit()
except Exception as e:
    print(f"FTP Error: {e}")
