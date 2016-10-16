import mechanize
from bs4 import BeautifulSoup
import sqlite3 as db

def oks_login(oks, username, passwd):
    login_status = False
    oks.open("http://www.okcupid.com")
    oks.form = list(oks.forms())[1]
    oks["username"] = username
    oks["password"] = passwd
    oks.submit()
    oks.open("http://www.okcupid.com")
    for link in oks.links():
        if link.text == "Sign Out":
            login_status = True
        else:
            pass
    return login_status


## Function to retrieve past contacts from file and then return in an array
def oks_past_matches(db_name,okc_username):
    try:
        con = db.connect(db_name)
        cur = con.cursor()
    except:
        print "[-] ERROR! Failed to Connect to Database\n\n"
        return
    past_matches = []
    try:
        raw_val = cur.execute("SELECT * FROM OKC_"+okc_username+"_matches")
        for line in raw_val:
            past_matches.append(str(line).split("'")[1])
        con.close()
    except:
        pass
    return past_matches


## Harvests Match IDs (Must be logged in)
def oks_harvest_match_ids(oks, db_name, username, past_matches):
    oks.open("http://www.okcupid.com/quickmatch")
    matches_index = []
    for link in oks.links():
        if "An image of " in str(link.text) and "[IMG]" in str(link.text) and " popover " not in str(link.text):
            matches_index.append(link.url.split('?')[0].split('/')[2])
    for match in matches_index:
        if match in past_matches:
            pass
        else:
            try:
                con = db.connect(db_name)
                cur = con.cursor()
            except:
                print "[-] ERROR! Failed to Connect to Database\n\n"
                return
            print match
            cur.execute("INSERT INTO OKC_"+username+"_matches VALUES('"+match+"','','','','','','','','','','','','','','','');")
            con.commit()
            con.close()


## Identify Profile User_ID 
def oks_get_user_id(oks, profile_id):
    response = oks.open("http://www.okcupid.com/profile/" + str(profile_id))
    soup = BeautifulSoup(response.read())
    scripts = soup.find_all("script")
    for script in scripts:
        if "FlagPhoto.ownerId" in str(script):
            user_id = str(script).split('"')[3]
    return user_id


## Favorite Profile (Must be logged in)
def oks_fav_profile(oks, own_user_id, target_user_id):
    oks.open("http://www.okcupid.com/vote_handler?target_userid="+str(target_user_id)+"&score=5&vote_type=personality&voterid="+str(own_user_id)+"&type=vote&cf=profile&target_objectid=0")


## Gather Profile Information Given Profile ID
def response_soup_scrape(oks, profile_id):
    response = oks.open("http://www.okcupid.com/profile/" + str(profile_id))
    soup = BeautifulSoup(response.read())
    title = soup.find_all("title")
    details_dict = {'profile_id': profile_id}
    details_dict['age'] = str(title).split(' / ')[1]
    details_dict['location'] = str(title).split(' / ')[2].split(' | ')[0]
    details_dict['orientation'] = str(soup.find_all("dd", attrs={'id':'ajax_orientation'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['ethnicity'] = str(soup.find_all("dd", attrs={'id':'ajax_ethnicities'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['height'] = str(soup.find_all("dd", attrs={'id':'ajax_height'})).split('>')[1].split('<')[0][:-2][2:].replace('\xe2\x80\xb2','\'').replace('\xe2\x80\xb3','"')
    details_dict['body'] = str(soup.find_all("dd", attrs={'id':'ajax_bodytype'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['diet'] = str(soup.find_all("dd", attrs={'id':'ajax_diet'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['smoker'] = str(soup.find_all("dd", attrs={'id':'ajax_smoking'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['alcohol'] = str(soup.find_all("dd", attrs={'id':'ajax_drinking'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['drugs'] = str(soup.find_all("dd", attrs={'id':'ajax_drugs'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['education'] = str(soup.find_all("dd", attrs={'id':'ajax_education'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['status'] = str(soup.find_all("dd", attrs={'id':'ajax_status'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['children'] = str(soup.find_all("dd", attrs={'id':'ajax_children'})).split('>')[1].split('<')[0][:-2][2:].replace('\xe2\x80\x99','\'')
    details_dict['pets'] = str(soup.find_all("dd", attrs={'id':'ajax_pets'})).split('>')[1].split('<')[0][:-2][2:]
    details_dict['lang'] = str(soup.find_all("dd", attrs={'id':'ajax_languages'})).split('>')[1].split('<')[0][:-2][2:]
    return details_dict    

