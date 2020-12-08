import numpy as np
import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import feature_selection
from joblib import dump
from statistics import mean 
import ModelHelperFunctions as mhf
import ModelHelperFunctions as mhf

#Calculate fscores for the entire dataset
df = pd.read_csv('data/stateDate.csv', header=0,delimiter=",")
y = df["new_death"].to_numpy()
X = df.drop("new_death", axis=1).to_numpy()

f_val, p_val = feature_selection.f_regression(X,y)
print("F values", f_val)

#Calculate fscores after dropping newCaseSum
dfDrop = df.drop("newCaseSum", axis=1)
XDrop = dfDrop.drop("new_death", axis=1).to_numpy()
f_val, p_val = feature_selection.f_regression(XDrop,y)
print("F values", f_val)

#Get signifcant variables for entire dataset
significantIDX = mhf.getSignificantIdx(X,y)
print("These indices are significant: ", significantIDX)

#Get significant variables after dropping newCaseSum
significantIDXDrop = mhf.getSignificantIdx(XDrop,y)
print("These indices are significant (when excluding new case sum): ", significantIDXDrop)

# Start a timer that we will later use to track runtime
start_time = time.time()

k = 10
permutations = [
    [0],
    [1],
    [2],
    [3],
    [4],
    [6],
    [7],
    [8],
    [0,1],
    [0,2],
    [1,2],
    [2,4],
    [3,6],
    [7,8],
    [0,1,2],
    [0,7,8],
    [1,7,8],
    [6,7,8],
    [0,1,2,3],
    [0,1,2,4],
    [0,1,7,8],
    [0,1,2,3,7,8],
    [0,1,2,3,4,7,8],
    [0,1,2,4,6,7,8],
    [0,1,2,3,4,6,7,8]
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
        start_fold_time = time.time()

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

        # end_fold_time = time.time()
        # fold_run_time = end_fold_time - start_fold_time
        # print("Runtime of Single Fold =", fold_run_time, "(s)")


    # # End of cross validation timer
    # end_time = time.time()
    # run_time = end_time - start_time
    # print("Total Runtime of Cross Validation =", run_time, "(s)")
    #print("Confidence Interval Cross validation scores:", cross_validation_ci_accuracy_scores)
    #print("CI interval margin =", np.round(ci_margins,0))
    print("Average CI accuracy =",
          np.round(sum(cross_validation_ci_accuracy_scores) / len(cross_validation_ci_accuracy_scores), 3))
    print("Average CI interval =", np.round(sum(ci_margins)/len(ci_margins),0))
    #print("Margin of Error Cross validation scores:", cross_validation_me_accuracy_scores)
    print("Average ME accuracy =",
          np.round(sum(cross_validation_me_accuracy_scores) / len(cross_validation_me_accuracy_scores), 3))
    print("Average MAE =",
          np.round(sum(maes) / len(maes), 3))
    print("Average RMSE =",
          np.round(sum(rmses) / len(rmses), 3))
    print()

    #Store trained tree as a file for quick running later
    # dump(d_tree, "Decision_Tree_Death_Count_Projection.joblib")