from twarc import Twarc #so we can access the Twitter API
import pandas as pd #so we can handle the dataset
import us #so we can process the US states easily
import calendar #so we can process month abbreviations
import fnmatch
import os

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
df = pd.read_csv(stateDateFileName, header=0, usecols=[0,1,3,4,5,6], delimiter=",")

#Remove rows that are not between the start and end dates specified
df = df[(df['submission_date'] >= startDate) & (df['submission_date'] <= endDate)]

#Add tweet count column
df["tweetCount"] = 0



###AGGREGATE TWITTER DATA

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

#Iterate through every date
for date in dates:
    print(date)
    #Create a stopping condition as API will time out
    if date > '05/01/2020':
        break
    stateCount = {}

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

    

    #Iterate through every tweet in the log
    for tweet in twarc.hydrate(dft):

        #Check to see if tweet originated from the US
        if (tweet["coordinates"] 
        and tweet["place"] is not None 
        and tweet["place"]["country_code"] is not None 
        and tweet["place"]["country_code"] == "US"):
            full_name = tweet["place"]["full_name"]
            state = ''

            #Washington, DC is included in the dataset, and obviously conflicts with Washington state, so we hadnle this case first
            if full_name == 'Washington, DC':
                state = 'DC'
            else:
                #find out what state it is
                matched = False
                #iterate through each abbreviation and see if it matches
                for abbr in stateAbbreviations:
                    if abbr in full_name:
                        state = abbr
                        matched = True
                #if a match before was not found, then iterate through the state names
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
        tweetCount = stateCount[state]
        df.loc[(df["submission_date"] == date) & (df["state"]==state), "tweetCount"] = tweetCount

                    


        
    




    

    


            



#Output the final dataframe for analysis
df.to_csv("../data/stateDate.csv", index=False)