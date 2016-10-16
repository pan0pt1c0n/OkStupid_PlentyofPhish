import mechanize
from bs4 import BeautifulSoup
import re

pop = mechanize.Browser()
pop.set_handle_robots(False)
pop.set_handle_refresh(False)

bot_name = "Leslie"
college_name = "University of Georgia"
state_name = "Georgia"

## Amanda20
pop.open("http://www.personalityforge.com/directchat.php?BotID=48646&MID=37471")

i=1
while i <= 100:
    pop.form = list(pop.forms())[0]
    pop["Message"] = str(raw_input("YOU - "))
    print "\n\n"
    response = pop.submit()
    soup = BeautifulSoup(response.read(),"lxml")
    divs = soup.find_all("div", attrs={'class':'theMessage bigfont'})
    reply = re.sub('<([^>]*)>','',str(divs)).replace('\\t','').replace('\\r','').replace('[','').replace(']','').split('\\n')[2]
    sanitized_reply = re.sub('Guest\d+','cutie',(reply.replace('Amanda',bot_name).replace('UCLA',college_name).replace('California',state_name)))
    if i == 5:
        print "HER - What was your first pet's name?\n\n"
    elif i == 10:
        print "HER - What was the first car you drove?\n\n"
    elif i == 15:
        print "HER - What is your mother's maiden name?\n\n"
    else:
        print "HER - " + sanitized_reply + "\n\n"
    i = i+1
