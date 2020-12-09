import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree, export_text
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import ModelHelperFunctions as mhf

# Massage data using data frames to get the feature variables for each sample and the label for each sample
df = pd.read_csv('data/stateDate.csv', header=0, delimiter=",")
y = df["new_death"].to_numpy()
X = df.drop("new_death", axis=1).to_numpy()

# Initialize variables that will be used later
k = 10
max_depths = [x for x in range(1,11)]

# Create a tree for each possible max depth and run k-fold validation on each tree
for max_depth in max_depths:
    print("max_depth =", max_depth)
    cross_validation_ci_accuracy_scores = []
    ci_margins = []
    cross_validation_me_accuracy_scores = []

    # K fold cross validation with prediction intervals
    for _ in range(k):
        # Split data into test and training data then train model and calculate standard deviation
        # of predictions on training data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle=True)
        d_tree = DecisionTreeRegressor(max_depth=max_depth).fit(X_train, y_train)
        std_dev_train = np.sqrt(sum((d_tree.predict(X_train) - y_train) ** 2) / len(y_train))

        # Make predictions
        y_predictions = d_tree.predict(X_test)

        # Evaluate the accuracy of the model on this training fold and store the accuracy score
        accuracy_ci,ci_margin = mhf.eval_accuracy_actual_within_confidence_interval(y_test=y_test, y_predictions=y_predictions, std_dev=std_dev_train)
        accuracy_me = mhf.eval_accuracy_margin_of_error_from_actual(y_test=y_test, y_predictions=y_predictions)

        # Store the results of the given fold
        cross_validation_ci_accuracy_scores.append(accuracy_ci)
        ci_margins.append(ci_margin)
        cross_validation_me_accuracy_scores.append(accuracy_me)

    # # start of Tree visualizing code - uncomment the code below to view the trees graphically or textually
    # # text visualization below
    # r = export_text(d_tree)
    # print(r)

    # # Graph visualization below
    # fig = plt.figure(figsize=(100,80))
    # _ = plot_tree(d_tree, filled=True)
    # fig.savefig("decision_tree_depth_{}".format(max_depth))

    # start Output for each decision tree - Gives the result of k-fold validation on each d tree
    print("Confidence Interval Cross validation scores:", cross_validation_ci_accuracy_scores)
    print("CI interval margin =", np.round(ci_margins,0))
    print("Average CI accuracy =",
          np.round(sum(cross_validation_ci_accuracy_scores) / len(cross_validation_ci_accuracy_scores), 2))
    print("Average CI interval =", np.round(sum(ci_margins)/len(ci_margins),0))
    print("Margin of Error Cross validation scores:", cross_validation_me_accuracy_scores)
    print("Average ME accuracy =",
          np.round(sum(cross_validation_me_accuracy_scores) / len(cross_validation_me_accuracy_scores), 2))
    print()