1. Twitter API is extremely easy to use. Got it figured out and I know how to get the data we need. You should both get Twitter developer accounts here: https://developer.twitter.com/en/apply-for-access
I roughly explained the project in terms of how Twitter was involved, just that we want to aggregate data from an IEEE dataport dataset based on location and that it's about COVID and that it's a course project, etc. Got instantly approved.
*NOTE: once you get your developer account, you will be given some keys and such. Those ethically should not be pushed to the repo, so save them somewhere... you need them in step 3!*

2. Install twarc, which is the python library to interface with the twitter API:

```
python3 -m pip install twarc
```

3. once twarc is installed, run:

```
twarc configure
```

It will ask you for the keys you gave. Will also ask if you want to use twitter to validate or manually do it each time (I told it to use Twitter and there was a very easy step to authorize that)

4. Also make sure you have pandas installed

5. Install this library that is a database of US states: us

```
python3 -m pip install us
```

6. Make an IEEE account (free) so that you can access the data files here: https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

7. The file `test.py` that would take one of those data files and hydrate the tweet IDs and determine the state where each tweet originated and the date it was tweeted... this should be a good shell for the rest of the dataprocessing we need to do.

8. NEXT STEPS: 
	1. What we will need is a way to aggregate the tweet counts by state (including DC). In my hastily made code, I'm just finding out what state it's from and what date it was tweeted, but we still need to somehow get a count of tweets per state per day. I'm thinking we can pretty easily automate the file processing, so the most "annoying" part should just be downloading the files and getting a loop set up to loop through each file.

	1. THEN we would need to download the CDC dataset and splice them together (so we should aggregate Tweets in a way that makes this easy). We also need to account that some states might not have any tweets on a given day (so this should be 0 tweets)