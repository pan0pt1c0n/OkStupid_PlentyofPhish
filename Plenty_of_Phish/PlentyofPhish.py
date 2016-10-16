import mechanize
from bs4 import BeautifulSoup
import sqlite3 as db

## Login with Provided Username and Password
def pof_login(pop, username, passwd):
    login_status = False
    pop.open("http://www.pof.com")
    pop.select_form("frmLogin")
    pop["username"] = username
    pop["password"] = passwd
    pop.submit()
    pop.open("http://www.pof.com")
    for link in pop.links():
        if link.text == "Log Out":
            login_status = True
        else:
            pass
    return login_status


## Function to retrieve past contacts from file and then return in an array
def pof_past_matches(db_name,pof_username):
    try:
        con = db.connect(db_name)
        cur = con.cursor()
    except:
        print "[-] ERROR! Failed to Connect to Database\n\n"
        return
    past_matches = []
    try:
        raw_val = cur.execute("SELECT * FROM POF_"+pof_username+"_matches")
        for line in raw_val:
            past_matches.append(str(line).split("'")[1])
        con.close()
    except:
        pass
    return past_matches


## Harvests Match IDs
def pof_harvest_match_ids(pop, db_name, pof_username, i):
    pop.open("http://www.pof.com/basicsearch.aspx")
    pop.select_form("form1")
    pop.submit()
    for link in pop.links():
        if "basicsearch.aspx?iama=" in link.url and link.text == '2':
            base_url = str(link.url).split('&count=')[0][:-1]
    pop.open("http://www.pof.com/"+base_url+str(i))
    matches_index = []
    for link in pop.links():
        if "viewprofile.aspx?profile_id=" in link.url and link.text == "[IMG]":
            matches_index.append(link.url.split('=')[1])
    for match in matches_index:
        try:
            con = db.connect(db_name)
            cur = con.cursor()
        except:
            print "[-] ERROR! Failed to Connect to Database\n\n"
            return
        print match
        cur.execute("INSERT INTO POF_"+pof_username+"_matches VALUES('"+match+"','','','','','','','','','','','','','','','','','','','','','');")
        con.commit()
        con.close()
    i = i+1
    return i


## Sends initial contact to matches (must be run after login and past_matches)
def pof_contact_matches(outfile, past_matches):
    matches_index = []
    pop.follow_link(text="My Matches")
    for link in pop.links():
        if "viewprofile.aspx?profile_id=" in link.url and link.text == "[IMG]":
            matches_index.append(link.url.split('=')[1])
    userfile = open(outfile,'a')
    
    for match in matches_index:
        if match in past_matches:
            pass
        else:
            userfile.write(str(match)+'\n')


## Gather Profile Information Given Profile ID
def response_soup_scrape(profile_id):
    response = pop.open("http://www.pof.com/viewprofile.aspx?profile_id=" + str(profile_id))
    soup = BeautifulSoup(response.read())
    spans = soup.find_all("span", attrs={'class':'txtGrey size15'})
    spans2 = soup.find_all("span", attrs={'class':'txtGrey size14'})
    divs = soup.find_all("div", attrs={'class':'profileheadcontent-narrow txtGrey size15'})
    details_dict = {'profile_id': profile_id}
    details_dict['username'] = str(spans[3]).split('\t')[10].split(' \r')[0]
    details_dict['location'] = str(divs).split('\t')[4].split('\r')[0]
    details_dict['age'] = str(spans[1]).split('\t')[5].split('\r')[0]
    details_dict['gender'] = str(spans[1]).split('\t')[15].split(',')[0]
    details_dict['height'] = str(spans[1]).split('\t')[20].split(',')[0]
    details_dict['religion'] = str(spans[1]).split('\t')[25].split('\r')[0]
    details_dict['ethnicity'] = str(spans[2]).split('\t')[5].split(',')[0]
    details_dict['sign'] = str(spans[2]).split('\t')[10].split('\r')[0]
    details_dict['education'] = str(spans[4]).split('\t')[5]
    details_dict['personality'] = str(spans[5]).split('\t')[5].split('\r')[0]
    details_dict['profession'] = str(spans[6]).split('\t')[5].split('\r')[0]
    details_dict['seeking'] = str(spans2[0]).split('\t')[7].split('<')[0]
    details_dict['agenda'] = str(spans2[1]).split('\t')[7].split('<')[0]
    details_dict['drinks'] = str(spans2[4]).split('\t')[7].split('<')[0]
    details_dict['marital'] = str(spans2[6]).split('\t')[7].split('<')[0]
    details_dict['drugs'] = str(spans2[7]).split('\t')[7].split('<')[0]
    details_dict['hair'] = str(spans2[8]).split('\t')[7].split('<')[0]
    details_dict['eyes'] = str(spans2[9]).split('\t')[7].split('<')[0]
    details_dict['car'] = str(spans2[10]).split('\t')[7].split('<')[0]
    details_dict['children'] = str(spans2[11]).split('\t')[7].split('<')[0]
    details_dict['longest_rel'] = str(spans2[12]).split('\t')[7].split('<')[0]
    return details_dict    


## Get Message Links of Logged In User and Output to messages_file.txt
def get_messages(outfile):
    response = pop.open("http://www.pof.com/inbox.aspx")
    mess_file = open(outfile,'a')
    for link in pop.links():
        if "viewallmessages.aspx?sender_id=" in link.url:
            mess_file.write(str(link.url)+'\n')
    more_pages = True
    while more_pages == True:
        try:
            response = pop.follow_link(text="Next Page")
            for link in pop.links():
                if "viewallmessages.aspx?sender_id=" in link.url:
                    mess_file.write(str(link.url)+'\n')
        except:
            more_pages = False
    mess_file.close()


## Read Messages from Input Message Link File and dump to specified output CSV
def read_messages(input_file, output_file):
    mess_file = open(input_file,'r')
    messages = []
    for line in mess_file:
        messages.append(line.strip())
    mess_file.close()
    output = open(output_file, 'a')
    for message in messages:
        try:
            response = pop.open("http://www.pof.com/" + str(message))
            soup = BeautifulSoup(response.read())
            mess_content = soup.find_all("div", attrs={'class':'message-content'})
            mess_output = ((str(mess_content).split(';">')[1]).split('<a href="sendmessage.aspx?usersendto=')[0]).replace(',','.')
            user_data = user_data = soup.find_all("span", attrs={'class':'username-inbox'})
            user_output = (str(user_data).split('">')[2]).split('</a>')[0]
            output.write(str(user_output) + ',' + str(mess_output) + '\n')
        except:
            pass
    output.close()


## Reply to All Existing Messages in Input File
def reply_to_all(input_file, replies_log, reply):
    mess_file = open(input_file,'r')
    messages = []
    for line in mess_file:
        messages.append(line.strip())
    mess_file.close()
    for message in messages:
        old_replies = open(replies_log, 'r')
        replies = []
        sender_id = message.split('sender_id=')[1].split('&')[0]
        for line in old_replies:
            replies.append(line.strip())
        old_replies.close()
        if sender_id in replies:
            pass
        else:
            outfile = open(replies_log, 'a')
            outfile.write(str(sender_id)+'\n')
            outfile.close()
            pop.open("http://www.pof.com/" + str(message))
            pop.select_form("sendmessage")
            pop["message"] = reply
            pop.submit()


## Delete All Existing Messages in Input File
def delete_messages(input_file):
    mess_file = open(input_file,'r')
    messages = []
    for line in mess_file:
        messages.append(line.strip())
    mess_file.close()
    for message in messages:
        pop.open("http://www.pof.com/" + str(message))
        pop.follow_link(text="Delete Conversation")

