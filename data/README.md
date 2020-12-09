<h1>Data files</h1>
This folder contains the data used to train our models:

- `stateTwitter.zip` contains a zip of the combined dataset used to train the models
- `stateTwitterResult.zip` contains a zip of data that we did not use to train the models, but is formatted like stateTwitter.zip
- `United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.zip` contains the CDC COVID-19 data
- `/tweet_logs` contains zipped lists of the tweet IDs used


<h2>Warning</h2>
Do not commit any files from the data folder into the git repository. The data files are too large for git and can cause problems. 
The .gitignore will hide csv files to prevent you from committing large files.

If you want to commit a data file, please zip the file and commit the zipped version. 
Only committing zipped files will keep the git repository small. To view the data, just unzip the existing zip files in this folder.
