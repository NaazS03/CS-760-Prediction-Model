def getSignificantIdx(X,y):
    import numpy as np
    """
    N = length(y)
    thetaMLE = inv(X'*X)*X'*y
    var = (y - X*thetaMLE)' * (y - X*thetaMLE) * (1/N)
    cov = var * inv(X'*X)
    isSignificant(i) = (thetaMLE(i) / cov(i,i)) > (3.8415)
    """
    significant = []
    N =  y.size
    xT = np.transpose(X)
    thetaMLE = np.matmul(np.matmul(np.linalg.inv(np.matmul(xT,X)),xT),y)
    var = (1.0/N) *np.matmul(np.transpose((y - np.matmul(X,thetaMLE))) , (y - np.matmul(X, thetaMLE)))
    cov = var * np.linalg.inv(np.matmul(xT,X)) 
    i = 0
    for theta in thetaMLE:
        if (thetaMLE[i] / cov[i][i]) > 3.8415:
            idx = i
            if i > 4:
                idx = idx + 1
            significant.append(idx)
        i = i + 1
    return significant


def gen_rmse(yTest, yPred):
    """
    Calculates the root mean squared error
    :param yTest: Test data labels
    :param yPred: Prediction data labels
    :return: The root mean squared error
    """
    from sklearn.metrics import mean_squared_error
    import numpy as np

    mse = mean_squared_error(yTest, yPred)
    rmse = np.sqrt(mse)
    return rmse

def gen_mae(yTest, yPred):
    """
    Calculates the mean absolute error
    :param yTest: Test data labels
    :param yPred: Prediction data labels
    :return: The mean absolute error
    """
    mae = 0
    for i in range(0, len(yPred)):
        prediction = yPred[i]
        actual = yTest[i]
        
        error = abs(actual - prediction)
        mae = mae + error
    mae = mae / len(yPred)
    return mae

def gen_confidence_intervals(means, std_dev):
    """
    Generates a list of confidence intervals
    :param means: a list of values - usually a list of label prediction values
    :param std_dev: The standard deviation on the training set of data
    :return: a list of confidence intervals
    """
    from scipy.stats import norm
    ppf = norm.ppf(0.975, loc=0, scale=1)
    # ppf = norm.ppf(0.95, loc=0, scale=1)
    interval_value = std_dev * ppf
    confidence_intervals = []

    for mean in means:
        upper = mean + interval_value
        lower = mean - interval_value
        confidence_intervals.append((lower, upper))

    return confidence_intervals,interval_value

def gen_margin_of_error_intervals(values):
    error_intervals = []
    margin_of_error = 0.1
    for value in values:
        interval_value = margin_of_error * value
        upper = value + interval_value
        lower = value - interval_value
        error_intervals.append((lower, upper))

    return error_intervals

def eval_accuracy_margin_of_error_from_actual(y_test, y_predictions):
    import numpy as np
    count_correct = 0.0
    y_test_intervals = gen_margin_of_error_intervals(y_test)
    num_test_samples = len(y_test)

    for sample_index in range(num_test_samples):
        y_interval = y_test_intervals[sample_index]
        y_lower_bound = y_interval[0]
        y_upper_bound = y_interval[1]
        y_prediction = y_predictions[sample_index]

        if y_lower_bound <= y_prediction and y_prediction <= y_upper_bound:
            count_correct+=1

    return np.round(count_correct / num_test_samples,2)

def eval_accuracy_actual_within_confidence_interval(y_test,y_predictions,std_dev):
    """
    Returns the percent of correct predictions on the provided test set.
    Predictions are correct if the actual label lies within the confidence interval
    :param y_test:  a list of test labels
    :param y_prediction_intervals: a list of prediction intervals
    :return: the percent of correct predictions
    """
    import numpy as np
    count_correct = 0.0
    num_test_samples = len(y_test)
    y_prediction_intervals, interval_value = gen_confidence_intervals(y_predictions,std_dev)

    for sample_index in range(num_test_samples):
        y_actual = y_test[sample_index]
        y_prediction_interval = y_prediction_intervals[sample_index]
        lower_bound = y_prediction_interval[0]
        upper_bound = y_prediction_interval[1]

        if lower_bound <= y_actual and y_actual <= upper_bound:
            count_correct+=1

    return np.round(count_correct / num_test_samples,2),interval_value

def convertStateAbbrToFips(abbr):
    import us
    stateAbbrMapping = us.states.mapping('abbr', 'fips')
    return stateAbbrMapping[abbr]

def convertFipstoAbbr(fips):
    import us
    stateFipsMapping = us.states.mapping('fips', 'abbr')
    return stateFipsMapping[fips]

def convertDateToUNIX(date):
    import pandas as pd
    return (pd.to_datetime(date) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

def convertUNIXToDate(unix):
    from datetime import datetime
    return datetime.fromtimestamp(unix)