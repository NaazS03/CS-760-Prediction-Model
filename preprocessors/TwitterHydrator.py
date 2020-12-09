from twarc import Twarc #Twitter API access
import pandas as pd #Dataset handling
import us #US State processing
import calendar #Month Abbreviations
import fnmatch #Filename matching
import os #Filename matching
import datetime #Timestamps
import json #Json processing

#Dictionary mapping months to month strings
monthAbbr = {
    '00' : '',
    '01' : 'january',
    '02' : 'february',
    '03' : 'march',
    '04' : 'april',
    '05' : 'may',
    '06' : 'june',
    '07' : 'july',
    '08' : 'august',
    '09' : 'september',
    '10' : 'october',
    '11' : 'november',
    '12' : 'december'
}

#Starting date to keep values
startDate = '04/01/2020'

#Ending date to keep values
endDate = '11/20/2020'

#Import the data of COVID cases every day by state
stateDateFileName = '../data/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv'
df = pd.read_csv(stateDateFileName, header=0, usecols=[0,1,3,4,5,6], delimiter=",")

#Remove rows that are not between the start and end dates specified
df = df[(df['submission_date'] >= startDate) & (df['submission_date'] <= endDate)]

#Get every date as a list
dates = df['submission_date'].unique()

#Specify twitter log directory
twitterDir = '../data/tweet_logs/tweet_logs_data_apr01_nov20/'

#Initialize the Twitter API Object
twarc = Twarc()

#Initialize list of all 50 states and the abbreviations
stateNames = [state.name for state in us.states.STATES]
stateAbbreviations = [state.abbr for state in us.states.STATES]
stateMapping = us.states.mapping('name', 'abbr')

allTweets = {}
#Iterate through every date
for date in dates:
    print(date)
    allTweets[date] = []
    #Find the corresponding twitter file for the date
    rawDate = date.split('/')
    month = rawDate[0]
    monthString = monthAbbr[month]
    keyString = monthString + str(int(rawDate[1]))
    fileName = ''
    for fname in os.listdir(twitterDir):
        rawFName = fname.split('_')
        fNameStart = rawFName[0]
        if keyString == fNameStart:
            fileName = fname
    
    #Verify file name has been set
    if fileName == '':
        continue

    #Read the corresponding twitter log
    dft=pd.read_csv(twitterDir + fileName, header=None)
    dft=dft[0]

    for tweet in twarc.hydrate(dft):
    
        #Check to see if tweet originated from the US
        if (tweet["coordinates"] 
        and tweet["place"] is not None 
        and tweet["place"]["country_code"] is not None 
        and tweet["place"]["country_code"] == "US"):
            #Store the tweet's geo-tagged information
            trimTweet = {}
            trimTweet["coordinates"] = tweet["coordinates"]
            trimTweet["place"] = {
                "country_code" : tweet["place"]["country_code"], 
                "full_name": tweet["place"]["full_name"]
            }
            allTweets[date].append(trimTweet)

#Store all the tweets as a json file
a_file = open("../data/tweet_logs/allTweets.json", "w")
json.dump(allTweets, a_file)
a_file.close()

