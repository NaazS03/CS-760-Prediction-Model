import numpy as np
import pandas as pd
import time
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from joblib import dump

import ModelHelperFunctions as mhf

# Start a timer that we will later use to track runtime
start_time = time.time()

# Massage data using data frames to get a the feature variables for each sample and the label for each sample
df = pd.read_csv('data/stateDate.csv', header=0, delimiter=",")
y = df["new_death"].to_numpy()
X = df.drop("new_death", axis=1).to_numpy()

k_fold = 10
num_neighbors = [x for x in range(1,11)]

for k_2 in num_neighbors:
    cross_validation_ci_accuracy_scores = []
    ci_margins = []
    cross_validation_me_accuracy_scores = []
    print("K =", k_2)
    # K fold cross validation with prediction intervals
    for _ in range(k_fold):
        start_fold_time = time.time()
        # Split data into test and training data then train model and calculate standard deviation
        # of predictions on training data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle=True)
        neigh = KNeighborsRegressor(n_neighbors=k_2, weights="distance").fit(X_train, y_train)
        pre = neigh.predict(X_train)
        sum1 = sum((neigh.predict(X_train) - y_train) ** 2)
        length = len(y_train)
        sqrt = np.sqrt(sum1/length)
        std_dev_train = np.sqrt(sum((neigh.predict(X_train) - y_train) ** 2) / len(y_train))

        # Make predictions
        y_predictions = neigh.predict(X_test)

        # Evaluate the accuracy of the model on this training fold and store the accuracy score
        accuracy_ci, ci_margin = mhf.eval_accuracy_actual_within_confidence_interval(y_test=y_test,
                                                                                     y_predictions=y_predictions,
                                                                                     std_dev=std_dev_train)
        accuracy_me = mhf.eval_accuracy_margin_of_error_from_actual(y_test=y_test, y_predictions=y_predictions)

        cross_validation_ci_accuracy_scores.append(accuracy_ci)
        ci_margins.append(ci_margin)
        cross_validation_me_accuracy_scores.append(accuracy_me)

        # end_fold_time = time.time()
        # fold_run_time = end_fold_time - start_fold_time
        # print("Runtime of Single Fold =", fold_run_time, "(s)")


    # End of cross validation timer
    # end_time = time.time()
    # run_time = end_time - start_time
    # print("Total Runtime of Cross Validation =", run_time, "(s)")
    print("Confidence Interval Cross validation scores:", cross_validation_ci_accuracy_scores)
    print("CI interval margin =", np.round(ci_margins, 0))
    print("Average CI accuracy =",
          np.round(sum(cross_validation_ci_accuracy_scores) / len(cross_validation_ci_accuracy_scores), 2))
    print("Average CI interval =", np.round(sum(ci_margins) / len(ci_margins), 0))
    print("Margin of Error Cross validation scores:", cross_validation_me_accuracy_scores)
    print("Average ME accuracy =",
          np.round(sum(cross_validation_me_accuracy_scores) / len(cross_validation_me_accuracy_scores), 2))
    print()