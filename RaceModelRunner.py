import numpy as np
import time
from joblib import load

start_time = time.time()

log_reg = load("Death_Given_Race_Model.joblib")

end_time = time.time()

run_time = end_time - start_time
print("Runtime of Race Model Loading =", run_time, "(s)")

for num in range(0,8):
    features = np.array([num]).reshape(1,-1)
    print("Prediction on", num, "=", log_reg.predict(features))
    print("Probability estimates for each class is", log_reg.predict_proba(features))