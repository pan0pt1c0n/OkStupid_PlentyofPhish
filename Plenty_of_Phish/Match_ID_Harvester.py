#!/usr/bin/python

import PlentyofPhish
import mechanize
import getpass
from bs4 import BeautifulSoup
import sys
from progressbar import ProgressBar

## Parameters !!!! MUST CHANGE !!!!
outfile = '/root/Projects/Plenty_of_Phish/logs/Scrape/Rd3/pof.log' ## TODO make dynamic
number_of_hits = 1000

## Define Bot Account
username = raw_input("Enter Bot Username: ")
passwd = getpass.getpass()
print "/n"

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

## File Length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

## Harvest Match IDs
length = 1
pbar = ProgressBar(maxval=number_of_hits).start()
i = 1
while length < number_of_hits:
    past_matches = PlentyofPhish.pof_past_matches(pop, outfile)
    i = PlentyofPhish.harvest_match_ids(pop, i, outfile, past_matches)
    length = file_len(outfile)
    pbar.update(length)
pbar.finish()
