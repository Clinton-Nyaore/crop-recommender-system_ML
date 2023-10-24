import joblib
import numpy as np
import pandas as pd
# Dump the trained classifier with joblib
DT_pkl_filename = 'DecisionTree.joblb'
# Open the file to save as pkl file


saved_model = joblib.load(DT_pkl_filename)


N = 83 
P = 45
K = 60
temperature =28
humidity = 70.3
ph = 7.0
rainfall = 150.9
data = np.array([[50.551818, 53.362727, 48.149091, 25.616244, 71.481779, 6.46948, 103.463655]])
data = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
print(f'prediction : {saved_model.predict(data)[0]}')