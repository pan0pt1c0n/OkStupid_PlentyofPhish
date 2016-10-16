#!/usr/bin/python

import PlentyofPhish
import mechanize
import getpass
from bs4 import BeautifulSoup
import sys

## Parameters !!!! MUST UPDATE !!!!
infile = "/root/Projects/Plenty_of_Phish/logs/Scrape/Rd3/pof.log"

## Define Bot Account
username = raw_input("Enter Bot Username: ")
passwd = getpass.getpass()
print "\n"

## Create Mechanize Browser Object
pop = mechanize.Browser()
pop.set_handle_robots(False)
pop.set_handle_refresh(False)

## Login with Bot
login = PlentyofPhish.pof_login(pop, username, passwd)
if login == True:
    print "[+] Login was Successful...\n"
else:
    print "[-] Login Failed...\n"
    sys.exit()

matches = []
login_status = True
matchfile = open(infile,'r')
for line in matchfile:
    matches.append(line.strip())
matchfile.close()

for match in matches:
    print "[+] Browsing to http://www.pof.com/viewprofile.aspx?profile_id=" + str(match) + "\n\n"
    pop.open("http://www.pof.com/viewprofile.aspx?profile_id=" + str(match))
    pop.follow_link(text="Add to Favorites!")
    for link in pop.links():
        if link.text == "Sign In":
            login_status = False
        else:
            pass
    if login_status == False:
        login = PlentyofPhish.pof_login(pop, username, passwd)
        if login == True:
            print "[+] Reinstantiating Session...\n"
            login_status = True
        else:
            print "[-] Reinstantiation Failed...\n"
            sys.exit()
