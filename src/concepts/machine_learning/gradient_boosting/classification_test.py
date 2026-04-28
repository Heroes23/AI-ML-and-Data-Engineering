import numpy as np
from gbdt_classifier import GradientBoostedClassifier
from sklearn.metrics import accuracy_score

# Create a random array
X = np.random.random(size=(10000, 5))
y = np.random.randint(0,1, size=(10000,))

# Range of the shape
shape_range = np.arange(X.shape[0], dtype=np.int32)

train_idx = np.random.choice(shape_range, size=(6000,), replace=False)

# Set comparison - What's in the bigger set that is not in the smaller set
test_idx = np.array([i for i in shape_range if i not in train_idx])

print(test_idx.shape)


X_train, y_train = X[train_idx], y[train_idx]

# Verify the shapes
print("Training set shapes")

print(X_train.shape)
print(y_train.shape)

X_test, y_test = X[test_idx], y[test_idx]

print("Test set shapes")

print(X_test.shape)
print(y_test.shape)

# Fit the GBDT Classifier
gbdt = GradientBoostedClassifier()

gbdt.fit(X=X_train, y=y_train)

# Predictions
y_pred = gbdt.predict(X=X_test)

# Basic accuracy
accuracy_mask = y_pred == y_test

print(accuracy_mask)

# Accuracy
accuracy = y_test[accuracy_mask].shape[0] / y_test.shape[0]

print(accuracy)

# Scikit-Learn Accuracy
sk_accuracy = accuracy_score(y_test, y_pred)

print(sk_accuracy)