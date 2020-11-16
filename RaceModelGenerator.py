import numpy as np
import time
from sklearn.linear_model import LogisticRegression
from joblib import dump,load

start_time = time.time()

data = np.loadtxt("data/Covid_Race_Death_Numerical_Data.csv", delimiter=",", skiprows=1)

x,y = data[:,0].reshape(-1,1),data[:,1]
log_reg = LogisticRegression(random_state=0).fit(x, y)

end_time = time.time()

run_time = end_time - start_time
print("Runtime of Race Model Training =", run_time, "(s)")

for num in range(0,8):
    features = np.array([num]).reshape(1,-1)
    print("Prediction on", num, "=", log_reg.predict(features))
    print("Probability estimates for each class is", log_reg.predict_proba(features))

dump(log_reg, "Death_Given_Race_Model.joblib")