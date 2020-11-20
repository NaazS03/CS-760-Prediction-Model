from twarc import Twarc #so we can access the Twitter API
import pandas as pd #so we can handle the dataset
import us #so we can process the US states easily
import calendar #so we can process month abbreviations

### Process the data file
# import original data
filename = "march20_march21"
dataframe=pd.read_csv("tweet_logs/" + filename + ".csv", header=None)

# grab only first column
dataframe=dataframe[0]

### Hydrate the tweets

# first, we will need a list of all 50 states and the abbreviations
state_names = [state.name for state in us.states.STATES]
state_abbreviations = [state.abbr for state in us.states.STATES]
name_to_abbr_mapping = us.states.mapping('name', 'abbr')

# for each tweet in the list, 
# if it is in the USA, 
# get the state its from
# HERE WE ARE ASSUMING THAT THE GEO-TAG OF A TWEET IS ACCURATE
# the variables we care about are date (around ln 49) and state (around ln 66 or 73)

#make the twitter api object
twarc = Twarc()
#iterate through each tweet, hydrating them along the way
for tweet in twarc.hydrate(dataframe):
	#only consider the tweet if it has location coordinates associated
	if tweet["coordinates"]:
		#traverse the tweet json structure to get to the location
		place = tweet["place"]
		if place is not None:
			#we are only looking at states in the USA
			if place["country_code"] is not None:
				if place["country_code"] == "US":
					print("new tweet from USA: " + str(tweet["id"]))
					#the date of the tweet
					raw_date = tweet["created_at"].split(" ")
					month = raw_date[1]
					month_num = str(list(calendar.month_abbr).index(month))
					if len(month_num) == 1:
						month_num = "0" + month_num
					day = raw_date[2]
					if len(day) == 1:
						day = "0" + day
					year = raw_date[5]
					date = month_num + "/" + day + "/" + year
					print("tweeted on " + date)

					#this gives the full name of the location,
					#of the form 'city, st' or 'state, usa'
					#we look for both
					full_name = place["full_name"]

					#Washington, DC is included in the dataset, and obviously conflicts with Washington state, so we hadnle this case first
					if full_name == 'Washington, DC':
						print(full_name + " is in " + "DC")
					else:
						#find out what state it is
						matched = False
						#iterate through each abbreviation and see if it matches
						for abbr in state_abbreviations:
							if abbr in full_name:
								state = abbr
								#print(full_name + " is in " + abbr)
								matched = True
						#if a match before was not found, then iterate through the state names
						if matched == False:
							for name in state_names:
								if name in full_name:
									state = name_to_abbr_mapping[name]
									#print(full_name + " is in " + state)
									matched = True

						#here, if we found the state, we print it, otherwise we cry
						if matched:
							print("tweeted from " + state)
						else:
							print("could not match " + full_name + " to a state :(")


