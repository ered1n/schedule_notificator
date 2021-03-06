import os
from pathlib import Path
import urllib.request
import filecmp
import smtplib
from email.message import EmailMessage
from datetime import date

DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

WEEK = str(date.today().isocalendar()[1])
URL = "https://rooster.talnet.nl/zuidoost/" + WEEK + "/c/c00045.htm"
STATUS = ["old", "new"]
SCHEDULE_OLD_EXISTS = Path("schedule_old.txt").is_file()

#SMTP
TO = ["2013917@talnet.nl", "2029870@talnet.nl", "acabrasnl@gmail.com", "ravidveeris@gmail.com"]
GMAIL_USER = "schedule.notification001@gmail.com"
GMAIL_PASS = "pythonproject"
SMTPSERVER = smtplib.SMTP("smtp.gmail.com", 587)
SMTPSERVER.ehlo()
SMTPSERVER.starttls()
SMTPSERVER.ehlo()
SMTPSERVER.login(GMAIL_USER, GMAIL_PASS)
HEADER = "To: " + ", ".join(TO) + "\n" + "From: " + GMAIL_USER + "\n" + "Subject: Rooster is gewijzigd \n"
CONTENT = "Het rooster is gewijzigd, kijk op " + URL + " voor de wijzigingen"
MSG = HEADER + "\n" + CONTENT

def getSchedule(url):
    try:
        return urllib.request.urlopen(url).read()
    except Exception as ex:
        return ex

def writeSchedule(status):
    filename = DIR  + "schedule_" + status + ".txt"
    with open(filename, "wb+") as txt_file:
        txt_file.write(getSchedule(URL))

def compare():
    return filecmp.cmp(DIR + "schedule_old.txt", DIR + "schedule_new.txt")

if(not SCHEDULE_OLD_EXISTS):
    writeSchedule(STATUS[0])

writeSchedule(STATUS[1])

if(not compare()):
    writeSchedule(STATUS[0])
    SMTPSERVER.sendmail(GMAIL_USER, TO, MSG)
    SMTPSERVER.close()
