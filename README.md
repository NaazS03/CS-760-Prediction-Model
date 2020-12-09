# Covid-19 Daily Death Prediction Models
The code in this repository was developed alongside the writing of the following research paper:

This repository contains a linear regression model and a decision tree regression model that will predict the number of
deaths that a state can expect on a given date based on CDC data and Tweets regarding Covid-19.

## Model Creation and Testing
To create and view the results of our model follow the steps below.

1. Go to the `/data` folder and unzip the file in their called `stateTwitter.zip`. This should create a .csv file in the data folder called `stateDate.csv`. The stateTwitter.zip file is a zipped version of the training data for the models we generate.

2. Run `DecisionTreeModelGenerator.py` or `LinRegModelGenerator.py`. In the terminal, you will see the output of 10-fold cross validation run on the model with a variety of configuration parameters. For more information about how the models are generated and tested, please view the comments in the python files mentioned earlier.
