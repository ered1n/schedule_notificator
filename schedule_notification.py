import os
from pathlib import Path
import urllib.request
import filecmp
import smtplib
from email.message import EmailMessage

os.system("cls" if os.name == "nt" else "clear")

URL = "https://rooster.talnet.nl/zuidoost/38/c/c00045.htm"
STATUS = ["old", "new"]
SCHEDULE_OLD_EXISTS = Path("schedule_old.txt").is_file()

#SMTP
TO = "2013917@talnet.nl"
GMAIL_USER = "schedule.notification001@gmail.com"
GMAIL_PASS = "pythonproject"
SMTPSERVER = smtplib.SMTP("smtp.gmail.com", 587)
SMTPSERVER.ehlo()
SMTPSERVER.starttls()
SMTPSERVER.ehlo()
SMTPSERVER.login(GMAIL_USER, GMAIL_PASS)
HEADER = "To: " + TO + "\n" + "From: " + GMAIL_USER + "\n" + "Subject: Rooster is gewijzigd \n"
CONTENT = "Het rooster is gewijzigd, kijk op https://rooster.talnet.nl/zuidoost/38/c/c00045.htm voor de wijzigingen"
MSG = HEADER + "\n" + CONTENT

def getSchedule(url):
    try:
        return urllib.request.urlopen(url).read()
    except Exception as ex:
        return ex

def writeSchedule(status):
    filename = "schedule_" + status + ".txt"
    with open(filename, "wb") as txt_file:
        txt_file.write(getSchedule(URL))

def compare():
    return filecmp.cmp("schedule_old.txt", "schedule_new.txt")

if(not SCHEDULE_OLD_EXISTS):
    writeSchedule(STATUS[0])

writeSchedule(STATUS[1])

if(compare()):
    print("Schedule has not changed.")
else:
    writeSchedule(STATUS[0])
    print("Schedule has changed.")
    try:
        SMTPSERVER.sendmail(GMAIL_USER, TO, MSG)
        print("Successfully sent email")
        SMTPSERVER.close()
    except SMTPException:
        print("Error: unable to send email")