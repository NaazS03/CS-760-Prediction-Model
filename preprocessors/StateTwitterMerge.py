import pandas as pd #Dataset handling
import us #US States library
import calendar #Handles month abbreviations
import fnmatch #Matching files
import os
import datetime #Timestamps
import json #Process json


#Starting date to keep values
startDate = '04/01/2020'

#Ending date to keep values
endDate = '11/20/2020'

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

###IMPORT STATE COVID DATA

#Import the data of COVID cases every day by state
stateDateFileName = '../data/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv'
df = pd.read_csv(stateDateFileName, header=0, usecols=[0,1,2,5,7,10], delimiter=",")

#Remove rows that are not between the start and end dates specified
df = df[(df['submission_date'] >= startDate) & (df['submission_date'] <= endDate)]

#Add tweet count and 14-day tweet sum
df["tweetCount"] = 0
df["twoWeekTweetSum"] = 0


###AGGREGATE TWITTER DATA

#Get every date as a list
dates = df['submission_date'].unique()

#Merge NY with NYC
df.loc[df["state"].str.contains('NY'), "state"] = 'NY'
df = df.groupby(["submission_date", "state"], as_index=False).agg("sum")

#Remove US territories other than Puerto Rico and Guam
weirdLocations = [
    'RMI',
    'GU',
    'AS',
    'MP',
    'FSM',
    'PW'
]
df.drop(df.loc[df['state'].isin(weirdLocations)].index, inplace=True)

#Initialize list of all 50 states and the abbreviations
stateNames = [state.name for state in us.states.STATES]
stateAbbreviations = [state.abbr for state in us.states.STATES]
stateMapping = us.states.mapping('name', 'abbr')

#Common misses and their respective states
missesMapping = {
    'San Francisco' : 'CA',
    'Virgin Islands' : 'VI', 
    'Las Vegas' : 'NV',
    'San Juan' : 'PR',
    'Puerto Rico' : 'PR',
    'Philadelphia' : 'PA',
    'Portland' : 'OR'
}

# Opening JSON file 
allTweets = {}
with open("../data/tweet_logs/allTweets.json") as json_file: 
    allTweets = json.load(json_file) 

#Iterate through every date
for date in dates:
    #Progress bar
    print(date)

    #List to hold the next 14 days
    futureDates = []

    #Obtain the month, day, and year of the date
    rawDate = date.split('/')
    month = int(rawDate[0])
    day = int(rawDate[1])
    year = int(rawDate[2])

    #Append the next 14 days to list
    d = datetime.datetime(year,month,day)
    for i in range(1,15):
        d += datetime.timedelta(days=1)
        currMonth = str(d.month)
        currYear = str(d.year)
        currDay = str(d.day)
        if len(currMonth) == 1:
            currMonth = "0" + currMonth 
        if len(currDay) == 1:
            currDay = "0" + currDay
        newFutureDate = currMonth + "/" + currDay + "/" + currYear
        if newFutureDate <= endDate:
            futureDates.append(newFutureDate)

    #Dictionary that holds tweet counts for a certain day
    stateCount = {}

    tweetsToday = allTweets[date]
    
    #Iterate through every tweet in the log
    for tweet in tweetsToday:
        #Check to see if tweet originated from the US
        if (tweet["coordinates"] 
        and tweet["place"] is not None 
        and tweet["place"]["country_code"] is not None 
        and tweet["place"]["country_code"] == "US"):
            full_name = tweet["place"]["full_name"]
            state = ''

            #Washington DC can conflict with Washington State and must be handled seperately
            if full_name == 'Washington, DC':
                state = 'DC'
            else:
                #Find out what state it is
                matched = False
                #Iterate through each abbreviation and see if it matches
                for abbr in stateAbbreviations:
                    if abbr in full_name:
                        state = abbr
                        matched = True
                #If a match before was not found, then iterate through the state names
                if matched == False:
                    for name in stateNames:
                        if name in full_name:
                            state = stateMapping[name]
                            matched = True
                #See if this is a common miss that is accounted for
                if matched == False:
                    for place in missesMapping.keys():
                        if place in full_name:
                            state = missesMapping[place]
                            matched = True


                #Increment the corresponding state if found
                if matched:
                    if state in stateCount:
                        stateCount[state] = stateCount[state] + 1
                    else:
                        stateCount[state] = 1

    #We now have the tweet count for a specific date
    for state in stateCount:
        #Store the tweet count in the correct cell
        tweetCount = stateCount[state]
        df.loc[(df["submission_date"] == date) & (df["state"]==state), "tweetCount"] = tweetCount

        #Add the tweet count to the next 14 days
        for currDate in futureDates:
            df.loc[(df["submission_date"] == currDate) & (df["state"]==state), "twoWeekTweetSum"] += tweetCount


#Convert the states to IDs
stateAbbrMapping = us.states.mapping('abbr','fips')
df["state"] = [stateAbbrMapping[x] for x in df["state"]]

#Convert to dates to timestamps
df["submission_date"] = [(pd.to_datetime(x) -  pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
                         for x in df["submission_date"]]

#Output the final dataframe for analysis
df.to_csv("../data/stateDate.csv", index=False)
