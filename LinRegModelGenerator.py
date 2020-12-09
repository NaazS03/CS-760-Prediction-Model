import numpy as np
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import feature_selection
from joblib import dump
from statistics import mean 
import ModelHelperFunctions as mhf

#Get signifcant variables for entire dataset
significantIDX = mhf.getSignificantIdx(X,y)
print("These indices are significant: ", significantIDX)

#Number of folds for cross-validation
k = 10

#Different permutations to run
permutations = [
    [6,7], #Twitter data only
    [0,1,2,3,4], #CDC data only
    [0,1,3,4,6], #Significant features only
    [0,1,2,3,4,6,7] #Every feature
]

for perm in permutations:
    print("Permutation =", perm)

    # Massage data using data frames to get a the feature variables for each sample and the label for each sample
    perm.append(5)
    df = pd.read_csv('data/stateDate.csv', header=0, usecols=perm, delimiter=",")
    y = df["new_death"].to_numpy()
    X = df.drop("new_death", axis=1).to_numpy()

    cross_validation_ci_accuracy_scores = []
    ci_margins = []
    cross_validation_me_accuracy_scores = []
    maes = []
    rmses = []

    # K fold cross validation with prediction intervals
    for _ in range(k):
        # Split data into test and training data then train model and calculate standard deviation
        # of predictions on training data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle=True)
        reg = LinearRegression().fit(X_train, y_train)
        std_dev_train = np.sqrt(sum((reg.predict(X_train) - y_train) ** 2) / len(y_train))

        # Make predictions
        y_predictions = reg.predict(X_test)

        # Evaluate the accuracy of the model on this training fold 
        accuracy_ci,ci_margin = mhf.eval_accuracy_actual_within_confidence_interval(y_test=y_test, y_predictions=y_predictions, std_dev=std_dev_train)
        accuracy_me = mhf.eval_accuracy_margin_of_error_from_actual(y_test=y_test, y_predictions=y_predictions)

        #Evalute MAE and RMSE
        mae = mhf.gen_mae(yTest=y_test, yPred = y_predictions)
        rmse = mhf.gen_rmse(yTest=y_test, yPred = y_predictions)

        #Store accuracy scores
        cross_validation_ci_accuracy_scores.append(accuracy_ci)
        ci_margins.append(ci_margin)
        cross_validation_me_accuracy_scores.append(accuracy_me)
        maes.append(mae)
        rmses.append(rmse)

        
    #Print all the values for the permuation
    print("Confidence Interval Cross validation scores:", cross_validation_ci_accuracy_scores)
    print("CI interval margin =", np.round(ci_margins,0))
    print("Average CI accuracy =",
          np.round(sum(cross_validation_ci_accuracy_scores) / len(cross_validation_ci_accuracy_scores), 3))
    print("Average CI interval =", np.round(sum(ci_margins)/len(ci_margins),0))
    print("Margin of Error Cross validation scores:", cross_validation_me_accuracy_scores)
    print("Average ME accuracy =",
          np.round(sum(cross_validation_me_accuracy_scores) / len(cross_validation_me_accuracy_scores), 3))
    print("Average MAE =",
          np.round(sum(maes) / len(maes), 3))
    print("Average RMSE =",
          np.round(sum(rmses) / len(rmses), 3))
    print()
