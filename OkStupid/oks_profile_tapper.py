#!/usr/bin/python

import OkStupid
import mechanize
import getpass
from bs4 import BeautifulSoup
import sys

## Parameters !!!! MUST UPDATE !!!!
infile = "/root/Projects/Bots/OkStupid/logs/oks.log" ## TODO Make this dynamic

## Define Bot Account
username = raw_input("Enter Bot Username (not email): ")
passwd = getpass.getpass()
print "/n"

## Create Mechanize Browser Object
oks = mechanize.Browser()
oks.set_handle_robots(False)
oks.set_handle_refresh(False)

## Get UserID
own_user_id = OkStupid.get_user_id(oks, username)

## Login with Bot
login = OkStupid.oks_login(oks, username, passwd)
if login == True:
    print "[+] Login was Successful...\n"
else:
    print "[-] Login Failed...\n"
    sys.exit()

## Staging
matches = []
login_status = True
matchfile = open(infile,'r')
for line in matchfile:
    matches.append(line.strip())
matchfile.close()

## Looping
for match in matches:
    print "[+] Browsing to - " + str(match) + "\n\n"
    target_user_id = OkStupid.get_user_id(oks, match)
    OkStupid.fav_profile(oks, own_user_id, target_user_id)
    for link in oks.links():
        if link.text == "Sign in":
            login_status = False
        else:
            pass
    if login_status == False:
        login = OkStupid.oks_login(oks, username, passwd)
        if login == True:
            print "[+] Reinstantiating Session...\n"
            login_status = True
        else:
            print "[-] Reinstantiation Failed...\n"
            sys.exit()
