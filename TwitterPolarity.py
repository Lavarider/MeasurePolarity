import twython as twy
import os
import time
import json
import regex as re
import datetime
import tweepy
from tweepy import Cursor
import snscrape.modules.twitter as sntwitter
import pandas as pd

from nltk.corpus import stopwords
from wordcloud import STOPWORDS
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from wordcloud import WordCloud
import chart_studio.plotly as py
from textblob import TextBlob
from nltk.text import Text
from pandas import Series
from plotly import tools
import networkx as nx
from PIL import Image
import seaborn as sns
import nltk, string
import pandas as pd
import numpy as np
import nltk as nlp
import warnings

begin_time = datetime.datetime.now()

# Set working directory
# this is where every csv file will be written to.
os.chdir(r'C:\Users\User\Desktop\FriendsOfPeopleFolder')   

APP_KEY = 'XXXX'
APP_SECRET = 'XXXX'
OAUTH_TOKEN = 'XXXX'
OAUTH_TOKEN_SECRET = 'XXXX'

# Connect
connection = twy.Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)


users=[]

# put directory/file with the @ IDS of the users you want to analyze in followerstest.txt.

with open(r"C:\Users\User\Desktop\followerstest.txt") as usersfile:
    for line in usersfile:
        users.append(line.rstrip())
print(users)

dems = []
repubs = []

# Dems.txt and Repubs.txt are included in the github repo, assign your own directory

with open(r'C:\Users\User\Desktop\dems.txt') as f:
    for line in f:
        dems.append(line)

with open(r'C:\Users\User\Desktop\Repubs.txt') as f:
    for line in f:
        repubs.append(line)


# Function to get friends
def get_friends(user, cursor, i=1, total_friends=None):
	try:
		print(('Getting friends for %s') % user)
		friendcount=0
		while cursor != '0':  # Cursor is a key returned by Twitter when there are more than 5,000 followers
			print(('Cursoring through friends.  On cursor %s') % cursor)
			friendcount=friendcount+1
			time.sleep(5)

			if int(friendcount)>3:
				adsflkj#purposely gibberish to stop program from taking super long

			temp = connection.get_friends_ids(screen_name=user, count=5000, cursor=cursor)  
			for entry in temp['ids']:  
				with open(r'C:\Users\User\Desktop\FriendsOfPeopleFolder/FriendsOf_' + user + '.txt', 'a') as f:
					#f.write(user + ',')
					f.write(str(entry) + '\n')  # Each ID is an integer, I make a string in order to write the newline string on the same line of code.

			cursor = temp['next_cursor_str']

	except(twy.TwythonRateLimitError):

		downloaded = 15 * 5000 * i  # Will be used to help monitor progress
		i += 1

		wait = 60 * 15 + 2   # how many seconds to wait

		print(('/n Stopped by Twitter rate limits.  Sleeping for %s minutes /n') % (wait / 60.0))

		if total_friends is not None:  # If the user provides total number of followers, print the below
			print(('Have downloaded %s of %s friends') % (downloaded, total_friends))

		print(('It is now %s') % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))  # So you know when to come back

		time.sleep(wait)  # Pause execution for wait seconds

		get_friends(user=user, cursor=cursor, total_friends=total_friends)  # Recursive, starts execution again

	except(twy.TwythonError, twy.TwythonAuthError(error_code=None, retry_after=None)) as e:
		print(e)

		get_friends(user=user, cursor=cursor, total_friends=total_friends)  # Recursive, starts execution again

		i += 1

monthlist=["July2019","August2019","September2019","October2019","November2019","December2019","January2020","Febuary2020","March2020","April2020","May2020","June2020","July2020","August2020","September2020","October2020","November2020","December2020","January2021","Febuary2021","March2021"]

monthdict={
"EarlyJuly2019": "2019-7-1",
"EarlyAugust2019": "2019-8-1",
"EarlySeptember2019": "2019-9-1",
"EarlyOctober2019": "2019-10-1",
"EarlyNovember2019": "2019-11-1",
"EarlyDecember2019": "2019-12-1",
"EarlyJanuary2020": "2020-1-1",
"EarlyFebuary2020": "2020-2-1",
"EarlyMarch2020": "2020-3-1",
"EarlyApril2020": "2020-4-1",
"EarlyMay2020": "2020-5-1",
"EarlyJune2020": "2020-6-1",
"EarlyJuly2020": "2020-7-1",
"EarlyAugust2020": "2020-8-1",
"EarlySeptember2020": "2020-9-1",
"EarlyOctober2020": "2020-10-1",
"EarlyNovember2020": "2020-11-1",
"EarlyDecember2020": "2020-12-1",
"EarlyJanuary2021": "2021-1-1",
"EarlyFebuary2021": "2021-2-1",
"EarlyMarch2021": "2021-3-1",

"LateJuly2019": "2019-7-29",
"LateAugust2019": "2019-8-29",
"LateSeptember2019": "2019-9-29",
"LateOctober2019": "2019-10-29",
"LateNovember2019": "2019-11-29",
"LateDecember2019": "2019-12-29",
"LateJanuary2020": "2020-1-29",
"LateFebuary2020": "2020-2-28",
"LateMarch2020": "2020-3-29",
"LateApril2020": "2020-4-29",
"LateMay2020": "2020-5-29",
"LateJune2020": "2020-6-29",
"LateJuly2020": "2020-7-29",
"LateAugust2020": "2020-8-29",
"LateSeptember2020": "2020-9-29",
"LateOctober2020": "2020-10-29",
"LateNovember2020": "2020-11-29",
"LateDecember2020": "2020-12-29",
"LateJanuary2021": "2021-1-29",
"LateFebuary2021": "2021-2-28",
"LateMarch2021": "2021-3-29"
}

monthtweetiddict={
'IDEarlyJuly2019': '1145482144636186624',
'IDLateJuly2019': '1155629004952494080',
'IDEarlyAugust2019': '1156716168419430401',
'IDLateAugust2019': '1166863028739923969',
'IDEarlySeptember2019': '1167950192303165441',
'IDLateSeptember2019': '1178097052519149568',
'IDEarlyOctober2019': '1178821828296548353',
'IDLateOctober2019': '1188968688407502849',
'IDEarlyNovember2019': '1190055852163682305',
'IDLateNovember2019': '1200202712350113793',
'IDEarlyDecember2019': '1200927488140095488',
'IDLateDecember2019': '1211074348381081601',
'IDEarlyJanuary2020': '1212161511977824256',
'IDLateJanuary2020': '1222308372160163847',
'IDEarlyFebuary2020': '1223395535765364737',
'IDLateFebuary2020': '1233542396069253121',
'IDEarlyMarch2020': '1233904783947333633',
'IDLateMarch2020': '1244051644133801986',
'IDEarlyApril2020': '1245138807743107074',
'IDLateApril2020': '1255285667967520768',
'IDEarlyMay2020': '1256010443753230341',
'IDLateMay2020': '1266157303939641347',
'IDEarlyJune2020': '1267244467578449921',
'IDLateJune2020': '1277391327718707202',
'IDEarlyJuly2020': '1278116103512711168',
'IDLateJuly2020': '1288262963762270210',
'IDEarlyAugust2020': '1289350127358894080',
'IDLateAugust2020': '1299496987528658945',
'IDEarlySeptember2020': '1300584151150735366',
'IDLateSeptember2020': '1310731011404247042',
'IDEarlyOctober2020': '1311455787189895169',
'IDLateOctober2020': '1321602647414214657',
'IDEarlyNovember2020': '1322689810990092289',
'IDLateNovember2020': '1332836671159754755',
'IDEarlyDecember2020': '1333561446945452037',
'IDLateDecember2020': '1343708307245117440',
'IDEarlyJanuary2021': '1344795470804054017',
'IDLateJanuary2021': '1354942331024273408',
'IDEarlyFebuary2021': '1356029494650413056',
#'IDLateFebuary2021': '1356029494650413056',
'IDLateFebuary2021': '1366029494650413056',
'IDEarlyMarch2021': '1366176354878824448',
'IDLateMarch2021': '1376323215132344326',
}

#sinceIDparamslist=[]
#maxIDparamslist=[]

#for month in monthlist:
#    earlyvar="Early"+month
#    sincedate=monthdict[earlyvar]
#    latevar="Late"+month
#    untildate=monthdict[latevar]

#    sinceIDparams="'"+"a "+"include:nativeretweets "+" until:"+sincedate+"'"
#    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(sinceIDparams).get_items()):
#        if i>1:
#            break
#    sinceIDparamslist.append([tweet.id])
#    idtweet1=str(tweet.id)
#    fullthing1="'"+"ID"+earlyvar+"': "+"'"+idtweet1+"',"
#    print(fullthing1)
#    sinceIDparamslist.clear()

#    maxIDparams="'"+"a "+"include:nativeretweets "+" until:"+untildate+"'"
#    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(maxIDparams).get_items()):
#        if i>1:
#            break
#    maxIDparamslist.append([tweet.id])
#    idtweet=str(tweet.id)
#    fullthing="'"+"ID"+latevar+"': "+"'"+idtweet+"',"
#    print(fullthing)
#    maxIDparamslist.clear()


usercountfortweepyorsnscrape=0

def gethistoricaltweets(user, month):

    global usercountfortweepyorsnscrape
    usercountfortweepyorsnscrape=usercountfortweepyorsnscrape+1
    print(usercountfortweepyorsnscrape)
    earlyvar="Early"+month
    sincedate=monthdict[earlyvar]
    latevar="Late"+month
    untildate=monthdict[latevar]

    earlyidvar="IDEarly"+month
    lateidvar="IDLate"+month
    sinceid=monthtweetiddict[earlyidvar]
    untilid=monthtweetiddict[lateidvar]

    # change if you want to only use snscrape or if you want to use both tweepy and snscrape
    #if (usercountfortweepyorsnscrape%2==0):
    if (usercountfortweepyorsnscrape%1==0):

#not including native retweets cause reddit doesnt have it

        #params = "'"+"include:nativeretweets "+"from:"+user+"'"
        params = "'"+"from:"+user+" since:"+sincedate+" until:"+untildate+"'"
        str(params)
        print(params)
        tweet_info=[]
        #time.sleep(4)

        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(params).get_items()):
            if i>3200:
                break
            tweet_info.append([user,tweet.content,tweet.date])
        tweetslistdataframe = pd.DataFrame(tweet_info, columns=["Handle",'Tweet',"Date"])
        if len(tweetslistdataframe)<10:
            time.sleep(3)
        if len(tweetslistdataframe)>1:
            tweetslistdataframe.to_csv(r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+"_tweets.csv")
        print(tweetslistdataframe)
        tweet_info.clear()
        del tweetslistdataframe

    else:
        print("on user", user) #gives constant feedback that the program is running
        tweet_info=[]
        #time.sleep(4)
            #try:
        #for tweet in Cursor(api.user_timeline, screen_name = user, tweet_mode="extended").items(3200): #extended tweet mode ensures we dont get weird truncation
        for tweet in Cursor(api.user_timeline, since_id = sinceid, max_id = untilid, screen_name = user, tweet_mode="extended").items(3200):
            #print(tweet.retweeted)
            if tweet.retweeted==False: #newline hope it works
                tweet_info.append([user, tweet.full_text,tweet.created_at])
                tweetslistdataframe=pd.DataFrame(tweet_info, columns=["Handle",'Tweet',"Date"])
        tweetslistdataframe.to_csv(r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+"_tweets.csv")
        print(tweetslistdataframe)
        if len(tweetslistdataframe)<10:
            time.sleep(3)
        tweet_info.clear()
        del tweetslistdataframe

politicalskew = 1
def setpoliticalskewto0():
	global politicalskew
	politicalskew = 0

def determineliberal(user):
	with open('FriendsOf_'+user+'.txt','r') as file1:
		with open(r'C:\Users\User\Desktop\shit\followersstuff/dems.txt') as file2:
				same = set(file1).intersection(file2)
				totdems=len(same)
				global politicalskew
				politicalskew=politicalskew+totdems
				print(user, "follows this many:", totdems, "liberals")

liberalslist=[]
nonpolarlist=[]
conservativelist=[]

def determineconservative(user):
	with open('FriendsOf_'+user+'.txt','r') as fileA:
		with open(r"C:\Users\User\Desktop\shit\followersstuff/repubs.txt") as repubfile:
				repubsame = set(fileA).intersection(repubfile)
				totrepubs=len(repubsame)
				global politicalskew
				politicalskew = politicalskew - totrepubs
				print(user, "follows this many:", totrepubs, "conservatives")
				print("this user skews politically", politicalskew)
				if politicalskew>3:
					liberalslist.append(user)
				elif 3>politicalskew>-3:
					nonpolarlist.append(user)
				else:
					conservativelist.append(user)

def openIDs(user):  # Read list of follower IDs
	id_file = 'FriendsOf_' + user + '.txt'
	ids = []
	with open(id_file) as f:
		temp = f.read().splitlines()
	for item in temp:
		ids.append(item.split(',')[1])  # First entry is screen name of user, 2nd entry is ID of follower
	return ids

#democrat=[]
#republican=[]

#democrat=pd.DataFrame(columns=["Tweet"])
#republican=pd.DataFrame(columns=["Tweet"])

#def assignpolarity(month):
#    for user in liberalslist:
#        global democrat
        #print("hi")
        #with open(r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+'_tweets.csv','r') as tweetfile:
#        try:
#            tweetfile=r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+'_tweets.csv'
#            tweetdataframe=pd.read_csv(tweetfile)
        #print(tweetdataframe)
        #democrat.append(tweetdataframe["Tweet"])
#            tweetslistdataframe=pd.DataFrame(tweetdataframe, columns=['Tweet'])
            #democratdict.append(tweetslistdataframe)
#            democrat=tweetslistdataframe["Tweet"].to_list()
            #democrat.append(tweetslistdataframe["Tweet"])
#        except:
#            print(user,"not",month)
        #democrat=tweetslistdataframe.tolist()
#    for user in conservativelist:
#        global republican
        #with open(r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+'_tweets.csv','r') as tweetfile1:
#        try:
#            tweetfile1=r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+'_tweets.csv'
#            tweetdataframe1=pd.read_csv(tweetfile1)
        #republican.append(tweetdataframe1["Tweet"])
#            tweetslistdataframe1=pd.DataFrame(tweetdataframe1, columns=['Tweet'])
            #republican=tweetslistdataframe1["Tweet"].to_list()
#            republican.append(tweetslistdataframe1)
            #republican.append(tweetslistdataframe1["Tweet"])
#        except:
#            print(user,"not",month)
        #democrat=tweetslistdataframe1.tolist()
    #print(democrat)

#democrat=pd.DataFrame(columns=["Handle",'Tweet',"Date"])
#republican=pd.DataFrame(columns=["Handle",'Tweet',"Date"])
democrat=[]
republican=[]

x=[]
y=[]

for month in monthlist:
    y.append(month)

def assignpolarity(month, user):
    global democrat
    global republican
    #with open(r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+'_tweets.csv') as tweetfile:
    if user in liberalslist:
        try:
            tweetfile=r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+'_tweets.csv'
            demtweetdataframe=pd.read_csv(tweetfile)
            democrat.append(demtweetdataframe["Tweet"].to_list())
        except:
            print(user,"is not on twitter during",month)
    if user in conservativelist:
        try:
            tweetfile=r"C:\Users\User\Desktop\FriendsOfPeopleFolder/"+user+"_"+month+'_tweets.csv'
            repubtweetdataframe=pd.read_csv(tweetfile)
        #print(repubtweetdataframe)
            republican.append(repubtweetdataframe["Tweet"].to_list())
        except:
            print(user,"is not on twitter during",month)


def calcpolarization(month):
    global democrat
    global republican


    STOPWORDS.add("rt")
    STOPWORDS.add("s")
    STOPWORDS.add("u")
    STOPWORDS.add("amp")
    STOPWORDS.add("th")
    STOPWORDS.add("will")
    STOPWORDS.add("t")
    STOPWORDS.add("m")

    #print(democrat)
    democratdataframe = pd.DataFrame(democrat)
    democratdataframegood=pd.Series(democratdataframe.values.ravel('F'))
    democratdataframegood.dropna(axis = 0, inplace = True)
    democratdataframegood=democratdataframegood.to_frame()
    democratdataframegood.columns=["Tweet"]

    repubdataframe = pd.DataFrame(republican)
    republicandataframegood=pd.Series(repubdataframe.values.ravel('F'))
    republicandataframegood.dropna(axis = 0, inplace = True)
    republicandataframegood=republicandataframegood.to_frame()
    republicandataframegood.columns=["Tweet"]
    #print(type(democratdataframegood))
    #print(democratdataframegood)
    #democrat=democrat.read()
    #democratstr=' '.join([str(elem) for elem in democrat])
    #Cleaning democrat party tweets
    democrat_list=[]
    for d in democratdataframegood.Tweet:
        d=re.sub(r'http\S+', '', d) #remove links
        d=re.sub("[^a-zA-Z]", " ", d) #remove all characters except letters
        d=d.lower() #convert all words to lowercase
        d=nltk.word_tokenize(d) #split sentences into word
        d=[word for word in d if not word in STOPWORDS] #remove the stopwords
        lemma=nlp.WordNetLemmatizer()
        d=[lemma.lemmatize(word) for word in d] #identify the correct form of the word in the dictionary
        d=" ".join(d)
        democrat_list.append(d)

    republican_list=[]
    for r in republicandataframegood.Tweet:
        r=re.sub(r'http\S+', '', r)
        r=re.sub("[^a-zA-Z]", " ", r)
        r=r.lower()
        r=nltk.word_tokenize(r)
        r=[word for word in r if not word in STOPWORDS]
        lemma=nlp.WordNetLemmatizer()
        r=[lemma.lemmatize(word) for word in r]
        r=" ".join(r)
        republican_list.append(r)

    #print(republican_list)

    demdemmatch=[]

    demsearchlist=["democrat", "dem","democ", 'liberal', "biden", "harris", "greennewdeal", "blm", "pro-choice",'agbecerra', 'alangrayson', 'angusking2018', 'anthonybrownmd4', 'barbaraboxer', 'bencardinformd', 'bennetforco', 'benniegthompson', 'berniesanders', 'bettymccollum04', 'billpascrell', 'bob_casey', 'bobbyscott', 'booker4senate', 'bradsherman', 'call_me_dutch', 'chriscoons', 'chrismurphyct', 'chrisvanhollen', 'clyburn', 'congressmanraja', 'congressmanruiz', 'corybooker', 'dwstweets', 'diannefeinstein', 'dickblumenthal', 'dickdurbin', 'donaldnorcross', 'dorismatsui', 'epwdems', 'edmarkey', 'eleanornorton', 'energydems', 'frankpallone', 'gkbutterfield', 'gerryconnolly', 'helpcmtedems', 'heidiheitkamp', 'heinrich4nm', 'hillaryclinton', 'housedemocrats', 'jecdems', 'jacksonleetx18', 'jeanneshaheen', 'jeffmerkley', 'jimlangevin', 'joaquincastrotx', 'joemanchinwv', 'johncarneyde', 'juliabrownley', 'juliabrownley26', 'kamalaharris', 'lacyclaymo1', 'lloyddoggetttx', 'lorettasanchez', 'mariacantwell', 'markwarner', 'martinheinrich', 'mccaskilloffice', 'menendez4nj', 'murraycampaign', 'nancypelosi', 'nelsonforsenate', 'nitalowey', 'normajtorres', 'nydiavelazquez', 'pattymurray', 'peterwelch', 'peters4michigan', 'repadamschiff', 'repadamsmith', 'repalgreen', 'repallawsonjr', 'repandrecarson', 'repannaeshoo', 'repanniekuster', 'repbrochester', 'repbarbaralee', 'repbarragan', 'repbeatty', 'repbera', 'repbetoorourke', 'repbillfoster', 'repbobbyrush', 'repbonamici', 'repbonnie', 'repbradashford', 'repbrady', 'repbrendanboyle', 'repbrianhiggins', 'repcarbajal', 'repcardenas', 'repcartwright', 'repcharliecrist', 'repcheri', 'repcicilline', 'repcohen', 'repcuellar', 'repcummings', 'repdankildee', 'repdannydavis', 'repdarrensoto', 'repdavideprice', 'repdesaulnier', 'repdebdingell', 'repdelbene', 'repdennyheck', 'repderekkilmer', 'repdianadegette', 'repdonbeyer', 'repdonaldpayne', 'repdwightevans', 'repebj', 'repeliotengel', 'repespaillat', 'repesty', 'repfilemonvela', 'repgaramendi', 'repgenegreen', 'repgracemeng', 'repgregorymeeks', 'repgutierrez', 'repgwenmoore', 'rephanabusa', 'rephankjohnson', 'rephastingsfl', 'rephuffman', 'repjackyrosen', 'repjaredpolis', 'repjayapal', 'repjeffries', 'repjerrynadler', 'repjimcosta', 'repjimmcdermott', 'repjimmypanetta', 'repjoecourtney', 'repjoekennedy', 'repjohnconyers', 'repjohndelaney', 'repjohnlarson', 'repjohnyarmuth', 'repjoseserrano', 'repjoshg', 'repjuanvargas', 'repjudychu', 'repkclark', 'repkarenbass', 'repkathleenrice', 'repkihuen', 'replawrence', 'replindasanchez', 'replipinski', 'reploiscapps', 'reploisfrankel', 'reploucorrea', 'replowenthal', 'replujangrisham', 'repmaloney', 'repmarciafudge', 'repmarcykaptur', 'repmarktakai', 'repmarktakano', 'repmaxinewaters', 'repmceachin', 'repmcgovern', 'repmcnerney', 'repmikehonda', 'repmikequigley', 'repohalleran', 'reppaultonko', 'repperlmutter', 'reppeteaguilar', 'reppeterdefazio', 'repraskin', 'repraulgrijalva', 'reprichardneal', 'reprichmond', 'repricklarsen', 'reprokhanna', 'reprobinkelly', 'repronkind', 'reproybalallard', 'reprubengallego', 'repsarbanes', 'repschakowsky', 'repschneider', 'repschrader', 'repscottpeters', 'repseanmaloney', 'repsheaporter', 'repsinema', 'repsires', 'repspeier', 'repstephmurphy', 'repstephenlynch', 'repsteveisrael', 'repsusandavis', 'repswalwell', 'repteddeutch', 'reptedlieu', 'repterrisewell', 'repthompson', 'reptimryan', 'reptimwalz', 'reptomsuozzi', 'repvaldemings', 'repveasey', 'repvisclosky', 'repwilson', 'repyvetteclarke', 'repzoelofgren', 'ronwyden', 'sanfordbishop', 'schatzforhawaii', 'senangusking', 'senbennetco', 'senbillnelson', 'senblumenthal', 'senbobcasey', 'senbooker', 'senbrianschatz', 'sencoonsoffice', 'sencortezmasto', 'sendonnelly', 'senduckworth', 'senfeinstein', 'senfranken', 'sengarypeters', 'sengillibrand', 'senjackreed', 'senjeffmerkley', 'senkaineoffice', 'senkamalaharris', 'senmarkey', 'sensanders', 'senschumer', 'sensherrodbrown', 'senstabenow', 'senwarren', 'senwhitehouse', 'sen_joemanchin', 'senateapprops', 'senatedems', 'senatorbaldwin', 'senatorbarb', 'senatorboxer', 'senatorcantwell', 'senatorcardin', 'senatorcarper', 'senatordurbin', 'senatorhassan', 'senatorheitkamp', 'senatorleahy', 'senatormenendez', 'senatorreid', 'senatorshaheen', 'senatortester', 'senatortomudall', 'senatorwarner', 'sherrodbrown', 'staceyplaskett', 'supjanicehahn', 'thedemocrats', 'tomcarperforde', 'tomudallpress', 'tulsipress', 'usrepkcastor', 'usrepkeating', 'usrepmikedoyle', 'usreprhinojosa', 'usrepricknolan', 'whiphoyer', 'wydenfororegon', 'wydenpress', 'alfranken', 'amyklobuchar', 'brianschatz', 'cbrangel', 'chakafattah', 'chelliepingree', 'chuckschumer', 'clairecmc', 'collinpeterson', 'coons4delaware', 'daveloebsack', 'dscc', 'elizabethforma', 'gracenapolitano', 'jahimes', 'janschakowsky', 'jontester', 'keithellison', 'louiseslaughter', 'mazieforhawaii', 'maziehirono', 'mikecapuano', 'nikiinthehouse', 'pedropierluisi', 'repbenraylujan', 'repblumenauer', "hillary","obama","nancypelosi", "aoc","cnn","prochoice","blacklivesmatter", "notmypresident", "thedailyshow","thenation","theyoungturks"]

    repubsearchlist=["republican", "repub","republi", "conservative", "trump", "pence", "pro-life",'austinscottga08', 'bankinggop', 'carlyfiorina', 'chrischristie', 'chuckgrassley', 'conawaytx11', 'congculberson', 'congmikesimpson', 'congressmandan', 'congressmangt', 'congressmanhice', 'danarohrabacher', 'darrellissa', 'drnealdunnfl2', 'drphilroe', 'epwgop', 'edworkforce', 'energygop', 'financialcmte', 'gop', 'gophelp', 'gopleader', 'gopsenfinance', 'gopoversight', 'goppolicy', 'govmikehuckabee', 'grahamblog', 'grassleypress', 'greggharper', 'hascrepublicans', 'herrerabeutler', 'houseadmngop', 'houseagnews', 'houseappropsgop', 'housecommerce', 'housegop', 'househomeland', 'housejudiciary', 'housescience', 'housesmallbiz', 'housevetaffairs', 'hurdonthehill', 'inhofepress', 'jebbush', 'jeffflake', 'jefffortenberry', 'jerrymoran', 'jiminhofe', 'jimpressoffice', 'jim_jordan', 'johnboozman', 'johncornyn', 'johnkasich', 'judgecarter', 'judgetedpoe', 'keithrothfus', 'kencalvert', 'lamarsmithtx21', 'mactxpress', 'mariodb', 'markamodeinv2', 'marshablackburn', 'mcconnellpress', 'mikecrapo', 'mikekellypa', 'natresources', 'pattiberi', 'patrickmchenry', 'petesessions', 'peterroskam', 'portmanpress', 'randpaul', 'raul_labrador', 'realbencarson', 'repabraham', 'repadriansmith', 'repandybarr', 'repandyharrismd', 'repannwagner', 'reparrington', 'repbillflores', 'repbilljohnson', 'repbillshuster', 'repblainepress', 'repbobgibbs', 'repbradwenstrup', 'repbrianbabin', 'repbrianmast', 'repbuddycarter', 'repbyrne', 'repcharliedent', 'repchriscollins', 'repchrissmith', 'repchrisstewart', 'repchuck', 'repcomstock', 'repcurbelo', 'repdlamborn', 'repdavejoyce', 'repdavid', 'repdavidvaladao', 'repdavidyoung', 'repdesantis', 'repdennisross', 'repdianeblack', 'repdougcollins', 'repdrewferguson', 'repedroyce', 'reperikpaulsen', 'repfranklucas', 'repfredupton', 'repfrenchhill', 'repgallagher', 'repgarretgraves', 'repgoodlatte', 'repgosar', 'repgusbilirakis', 'repguthrie', 'rephalrogers', 'rephartzler', 'rephensarling', 'repholding', 'rephuizenga', 'rephultgren', 'repjbridenstine', 'repjackbergman', 'repjasonlewis', 'repjasonsmith', 'repjeffdenham', 'repjeffduncan', 'repjimbanks', 'repjimrenacci', 'repjoebarton', 'repjoewilson', 'repjohnfaso', 'repjohnkatko', 'repkaygranger', 'repkenbuck', 'repkenmarchant', 'repkevinbrady', 'repkevincramer', 'repkevinyoder', 'repkinzinger', 'repkristinoem', 'replahood', 'replamalfa', 'replancenj7', 'replarrybucshon', 'repleezeldin', 'replobiondo', 'reploubarletta', 'reploudermilk', 'replukemesser', 'replynnjenkins', 'repmgriffith', 'repmarkmeadows', 'repmarkwalker', 'repmartharoby', 'repmccaul', 'repmcclintock', 'repmckinley', 'repmeehan', 'repmialove', 'repmikebishop', 'repmikecoffman', 'repmikerogersal', 'repmiketurner', 'repmimiwalters', 'repmobrooks', 'repmoolenaar', 'repmullin', 'repnewhouse', 'reppaulcook', 'reppaulmitchell', 'reppeteking', 'reppeteolson', 'reppoliquin', 'reprwilliams', 'repralphnorman', 'reprichhudson', 'reprickallen', 'reprobbishop', 'reprodblum', 'reprussell', 'repryancostello', 'repryanzinke', 'repsanfordsc', 'repscottperry', 'repseanduffy', 'repshimkus', 'repsmucker', 'repstefanik', 'repstevepearce', 'repstevestivers', 'reptedyoho', 'repthomasmassie', 'reptipton', 'reptomemmer', 'reptomgarrett', 'reptomgraves', 'reptommacarthur', 'reptommarino', 'reptomprice', 'reptomreed', 'reptomrice', 'reptrentfranks', 'reptrey', 'repwalberg', 'repwalorski', 'repwalterjones', 'repwebster', 'repwesterman', 'rep_hunter', 'republicanstudy', 'robwittman', 'robert_aderholt', 'rodneydavis', 'roslehtinen', 'royblunt', 'roybluntpress', 'rulesreps', 'sascmajority', 'samspressshop', 'senalexander', 'senbobcorker', 'sencapito', 'sencorygardner', 'sendansullivan', 'sendeanheller', 'senjohnbarrasso', 'senjohnhoeven', 'senjohnkennedy', 'senjohnmccain', 'senjohnthune', 'senjoniernst', 'senmikelee', 'senpatroberts', 'senronjohnson', 'senrubiopress', 'sensasse', 'sentedcruz', 'senthadcochran', 'senthomtillis', 'sentoddyoung', 'sentomcotton', 'sentoomey', 'senatecommerce', 'senategop', 'senatemajldr', 'senaterpc', 'senatorburr', 'senatorcollins', 'senatorenzi', 'senatorfischer', 'senatorisakson', 'senatorlankford', 'senatorrisch', 'senatorrounds', 'senatortimscott', 'senatorwicker', 'speakerryan', 'stevedaines', 'stevekingia', 'stevescalise', 'susanwbrooks', 'tgowdysc', 'txrandy14', 'toddrokita', 'tomcoleok04', 'tomrooney', 'transport', 'usrepgarypalmer', 'usreplong', 'usreprodney', 'vernbuchanan', 'warrendavidson', 'waysandmeansgop', 'amashoffice', 'boblatta', 'cathymcmorris', 'congbillposey', 'davereichert', 'farenthold', 'housebudgetgop', 'lisamurkowski', 'marcorubio', 'michaelcburgess', 'mike_pence', 'rep_stevewomack', 'repdavetrott', 'repdonyoung', 'repgregwalden', 'replouiegohmert', 'reppittenger', 'senategopfloor', 'sendavidperdue', 'senorrinhatch', 'senrobportman', 'tedcruz', 'virginiafoxx', "gop", "maga", "makeamericagreatagain","americafirst","foxnews","prolife","keepamericagreat","bluelivesmatter","alllivesmatter", "crowder", "shapiro","mattwalsh", "charliekirk","newsmax","oann","realcandaceo","hawleymo","realmattcouch","greene","tucker"]

    print("DURING THE MONTH OF:",month)

    for word in demsearchlist:
        regex="((?:\S+\s+){0,5}"+word+"\s*(?:\S+\s+){0,5})"
        for i in democrat_list:
            if re.search(regex, str(i)):
                demdemmatch.append(i)
    #print(demdemmatch)
    democratblob=TextBlob(str(demdemmatch))
    demdemsentiment=democratblob.sentiment.polarity
    print(demdemsentiment)

    demrepubmatch=[]
    for word in repubsearchlist:
        regex="((?:\S+\s+){0,5}"+word+"\s*(?:\S+\s+){0,5})"
        for i in democrat_list:
            if re.search(regex, str(i)):
                demrepubmatch.append(i)
    #print(demrepubmatch)
    democratrepubblob=TextBlob(str(demrepubmatch))
    demrepubsentiment=democratrepubblob.sentiment.polarity
    print(demrepubsentiment)

    dempolarity=demdemsentiment-demrepubsentiment
    print("dempolarity is:", dempolarity)

    repubrepubmatch=[]
    for word in repubsearchlist:
        regex="((?:\S+\s+){0,5}"+word+"\s*(?:\S+\s+){0,5})"
        for i in republican_list:
            if re.search(regex, str(i)):
                repubrepubmatch.append(i)
    #print(repubrepubmatch)
    repubrepubblob=TextBlob(str(repubrepubmatch))
    repubrepubsentiment=repubrepubblob.sentiment.polarity
    print(repubrepubsentiment)

    repubdemmatch=[]
    for word in demsearchlist:
        regex="((?:\S+\s+){0,5}"+word+"\s*(?:\S+\s+){0,5})"
        for i in republican_list:
            if re.search(regex, str(i)):
                repubdemmatch.append(i)
    #print(repubdemmatch)
    repubdemblob=TextBlob(str(repubdemmatch))
    repubdemsentiment=repubdemblob.sentiment.polarity
    print(repubdemsentiment)

    repubpolarity=repubrepubsentiment-repubdemsentiment

    print("repubpolarity is:", repubpolarity)

    for i in monthlist:
        overallpolarity=(repubpolarity+dempolarity)/2
    x.append(overallpolarity)

    democrat.clear()
    republican.clear()
    demdemmatch.clear()
    demrepubmatch.clear()
    repubdemmatch.clear()
    repubrepubmatch.clear()


#for month in monthlist:
    #print("On Month:",month)
    #for user in users:
    #    try:
    #        gethistoricaltweets(user=user, month=month)
    #    except:
    #        print(user,"is not on twitter during",month,"month")

# The below code gets the following list and the users tweets

for user in users:
    time.sleep(5)
    print("On user",user)
    try:
        account = connection.lookup_user(screen_name=[user])
        account_id = account[0]['id']  # The ID number for the user in the account object
        get_friends(user=user, cursor=-1)# No object saved to because the function writes to file instead.  cursor needs to be any number not equal to 0.
    except:
        print(user,"is not on twitter")
        time.sleep(45)

    for month in monthlist:
        try:
            gethistoricaltweets(user=user, month=month)
            time.sleep(1)
        except:
            print(user,"is not on twitter during the month of", month)
            time.sleep(1)

# the below code assigns users to a political side

for user in users:
    try:
        setpoliticalskewto0()
        determineliberal(user=user)
        determineconservative(user=user)
    except:
        print(user, "is not on twitter")

# the below code calculates the polarization across the corpus

for month in monthlist:
    for user in users:
        assignpolarity(month=month, user=user)

    calcpolarization(month=month)

print(x)
print(y)

plt.plot(y, x)

# naming the x axis
plt.xlabel('Dates',rotation=90)
# naming the y axis
plt.ylabel('Polarity')

# giving a title to my graph
plt.title('Polarization Over Time!')

# use cnn and fox news as a baseline

#filter out news outlets by followers

# function to show the plot
plt.show()

print("There were this many liberals:", liberalslist)
print("There were this many nonpolars", nonpolarlist)
print("There were this many conservatives", conservativelist)

print("all done!")

print(datetime.datetime.now() - begin_time)
