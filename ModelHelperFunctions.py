from scipy.stats import norm

def gen_confidence_intervals(means, std_dev):
    """
    Generates a list of confidence intervals
    :param means: a list of values - usually a list of label prediction values
    :param std_dev: The standard deviation on the training set of data
    :return: a list of confidence intervals
    """
    ppf = norm.ppf(0.975, loc=0, scale=1)
    interval_value = std_dev * ppf
    confidence_intervals = []

    for mean in means:
        upper = mean + interval_value
        lower = mean - interval_value
        confidence_intervals.append((lower, upper))

    return confidence_intervals


def eval_accuracy(y_test, y_prediction_intervals):
    """
    Returns the percent of correct predictions on the provided test set.
    Predictions are correct if the actual label lies within the confidence interval
    :param y_test:  a list of test labels
    :param y_prediction_intervals: a list of prediction intervals
    :return: the percent of correct predictions
    """
    count_correct = 0.0
    num_test_samples = len(y_test)
    for sample_index in range(num_test_samples):
        y_actual = y_test[sample_index]
        y_prediction_interval = y_prediction_intervals[sample_index]
        lower_bound = y_prediction_interval[0]
        upper_bound = y_prediction_interval[1]

        if lower_bound <= y_actual and y_actual <= upper_bound:
            count_correct+=1

    return count_correct / num_test_samples

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