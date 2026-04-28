import numpy as np
from decision_tree_regression import RegressionTree

# Farenheit to Celsius

X = [32, 33, 70, 70, 90, 95]
y = [0, 0.555, 21.111, 21.111, 32.222, 35]

# Regression Tree
rt = RegressionTree()

# Reshape X to be a 2-D matrix
X = np.array(X).reshape(-1, 1)
y = np.array(y)

# Fit on the data
rt.fit(X=X, y=y)

# New sample for X
x_sample = np.array([72]).reshape(-1,1)

y_pred = rt.predict(X=x_sample)

print(y_pred)
