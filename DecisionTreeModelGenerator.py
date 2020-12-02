import numpy as np
import pandas as pd
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from joblib import dump

import ModelHelperFunctions as mhf

# Start a timer that we will later use to track runtime
start_time = time.time()

# Massage data using data frames to get a the feature variables for each sample and the label for each sample
df = pd.read_csv('data/stateDate.csv', header=0, delimiter=",")
y = df["new_death"].to_numpy()
X = df.drop("new_death", axis=1).to_numpy()
k = 5 #10
max_depth = 1
cross_validation_accuracy_scores = []
decision_trees = []
std_deviations = []

# K fold cross validation with prediction intervals
for _ in range(k):
    start_fold_time = time.time()

    # Split data into test and training data then train model and calculate standard deviation
    # of predictions on training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle=True)
    d_tree = DecisionTreeRegressor(max_depth=max_depth).fit(X_train, y_train)
    std_dev_train = np.sqrt(sum((d_tree.predict(X_train) - y_train) ** 2) / len(y_train))

    # Use the model and standard deviation on training data to generate confidence intervals for predictions
    y_predictions = d_tree.predict(X_test)
    y_prediction_intervals = mhf.gen_confidence_intervals(means=y_predictions, std_dev=std_dev_train)

    # Evaluate the accuracy of the model on this training fold and store the accuracy score
    accuracy = mhf.eval_accuracy(y_test=y_test, y_prediction_intervals=y_prediction_intervals)
    cross_validation_accuracy_scores.append(accuracy)
    decision_trees.append(d_tree)
    std_deviations.append(std_dev_train)

    end_fold_time = time.time()
    fold_run_time = end_fold_time - start_fold_time
    print("Runtime of Single Fold =", fold_run_time, "(s)")


# End of cross validation timer
end_time = time.time()
run_time = end_time - start_time
print("Total Runtime of Cross Validation =", run_time, "(s)")
print("Cross validation scores:",cross_validation_accuracy_scores)

#Store trained tree as a file for quick running later
# dump(d_tree, "Decision_Tree_Death_Count_Projection.joblib")