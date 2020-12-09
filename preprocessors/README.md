<h1>Dataset Creation & Processing</h1>
We provide the completed dataset in the `/data` folder from the main repo. However this folder contains details on how to recreate or extend the dataset, which we created by stitching together Twitter data with data from the CDC. The process to gain access to both datasets and also to run the scripts to create a usable dataset are outlined below:

1. You need access to the Twitter API in order to hydrate the tweets. You should both get Twitter developer accounts here: https://developer.twitter.com/en/apply-for-access
*NOTE: once you get your developer account, you will be given some keys and such. Those ethically should not be pushed to the repo, so save them somewhere... you need them in step 3!*

2. Install twarc, which is the python library to interface with the twitter API:

```
python3 -m pip install twarc
```

3. once twarc is installed, run:

```
twarc configure
```

It will ask you for the keys you were given.

4. Also make sure you have pandas installed

5. Install this library that is a database of US states: us

```
python3 -m pip install us
```

6. Make an IEEE account (free) so that you can access the data files here: https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

7. Note that you need `data/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.zip` to be unzipped in the `/data` folder and `/data/tweet_logs/tweet_logs_data_apr01_nov20.zip` to be unzipped in the `/data/tweet_logs` folder.

8. Once all the required data from 7. is in the `/data` folder as .csv files then you can run the preprocessors. 

9. Run the `TwitterHydrator.py` preprocessor first and then run the `StateTwitterMerge.py`. `TwitterHydrator.py` will get the information we are interested in from the tweet ids stored in `/data/tweet_logs`. `StateTwitterMerge.py` will merge the CDC gathered COVID-19 data with the twitter information we gathered.

10. Now all the data is fully preprocessed and either of the model generatory python files can be ran successfully as discussed in the main `README.md`.
