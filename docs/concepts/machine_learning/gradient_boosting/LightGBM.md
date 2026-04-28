## LightGBM (Light Gradient Boosting Machine)

### Topics

1. Introduction to LightGBM
2. Key Innovations
3. Gradient-based One-Side Sampling (GOSS)
4. Exclusive Feature Bundling (EFB)
5. Leaf-wise Tree Growth
6. Python Implementation - Classifier - LightGBM
7. Python Implementation - Regressor - LightGBM
8. Hyperparameter Tuning

### Introduction to LightGBM

- LightGBM is a gradient boosting framework developed by Microsoft that uses tree-based learning algorithms.
- It is designed to be distributed and efficient with the following advantages:
    - Faster training speed and higher efficiency
    - Lower memory usage
    - Better accuracy
    - Support for parallel and GPU learning
    - Capable of handling large-scale data

- LightGBM builds trees leaf-wise (best-first) rather than level-wise like traditional gradient boosting methods.
    - This approach can converge much faster but may be prone to overfitting if not properly controlled.

### Key Innovations

LightGBM introduces two novel techniques that significantly improve training speed and memory efficiency:

1. **Gradient-based One-Side Sampling (GOSS)**
   - Keeps instances with large gradients
   - Randomly samples instances with small gradients
   - Reduces computation while maintaining accuracy

2. **Exclusive Feature Bundling (EFB)**
   - Bundles mutually exclusive features together
   - Reduces the number of features
   - Decreases memory usage without loss of information

### Gradient-based One-Side Sampling (GOSS)

#### Concept

- In gradient boosting, data instances with larger gradients contribute more to information gain.
- GOSS retains instances with large gradients and performs random sampling on instances with small gradients.

#### Algorithm Steps

1. Sort the data instances by the absolute value of their gradients in descending order.
2. Select the top $a \times 100\%$ instances with the largest gradients.
3. Randomly sample $b \times 100\%$ of instances from the remaining data.
4. Amplify the sampled small gradient instances by a constant factor $\frac{1-a}{b}$ when computing information gain.

#### Mathematical Formulation

For a feature $j$ at split point $d$:

$$\text{Gain}_j(d) = \frac{1}{n}\left(\frac{(\sum_{x_i \in A_l}g_i)^2}{n_l^j(d)} + \frac{(\sum_{x_i \in A_r}g_i)^2}{n_r^j(d)}\right)$$

Where:
- $g_i$ is the gradient of the loss function with respect to the prediction for instance $i$
- $A_l$ and $A_r$ are the left and right child nodes after the split
- $n_l^j(d)$ and $n_r^j(d)$ are the number of instances in the left and right nodes

With GOSS, small gradient instances are amplified:

$$\text{Gain}_j^{GOSS}(d) = \frac{1}{n}\left(\frac{(\sum_{x_i \in A_l \cap Top_a}g_i + \frac{1-a}{b}\sum_{x_i \in A_l \cap Random_b}g_i)^2}{n_l^j(d)} + \frac{(\sum_{x_i \in A_r \cap Top_a}g_i + \frac{1-a}{b}\sum_{x_i \in A_r \cap Random_b}g_i)^2}{n_r^j(d)}\right)$$

#### Benefits

- Reduces the number of instances used in information gain calculation
- Maintains focus on instances that matter most (large gradients)
- Significantly speeds up training

### Exclusive Feature Bundling (EFB)

#### Concept

- High-dimensional data often has many sparse features (features that rarely take non-zero values simultaneously).
- These mutually exclusive features can be safely bundled together into a single feature.

#### Algorithm Steps

1. Construct a graph where features are nodes.
2. Add edges between features that are not mutually exclusive.
3. Perform graph coloring to find bundles (features with the same color are bundled).
4. Merge features in the same bundle by adding offsets to feature values.

#### Example

Consider two binary features $F_1$ and $F_2$ that are mutually exclusive:

| Sample | $F_1$ | $F_2$ | Bundled Feature |
|--------|-------|-------|-----------------|
| 1      | 0     | 0     | 0               |
| 2      | 1     | 0     | 1               |
| 3      | 0     | 1     | 2               |
| 4      | 0     | 0     | 0               |

The bundled feature uses value 1 for $F_1=1$ and value 2 for $F_2=1$.

#### Benefits

- Reduces the number of features without information loss
- Decreases memory usage
- Speeds up tree construction

### Leaf-wise Tree Growth

#### Traditional Level-wise Growth

- Grows tree level by level
- Splits all nodes at the same depth
- More conservative, less prone to overfitting
- May be inefficient as it splits nodes with little information gain

#### LightGBM's Leaf-wise Growth

- Grows tree by splitting the leaf with the maximum delta loss (best-first)
- Can achieve lower loss than level-wise growth with the same number of splits
- More aggressive, can converge faster
- May overfit if not controlled with `max_depth` or `num_leaves`

#### Comparison Visualization

```
Level-wise (XGBoost):
       Root
      /    \
    N1      N2
   /  \    /  \
  L1  L2  L3  L4

Leaf-wise (LightGBM):
       Root
      /    \
    N1      L1
   /  \
  N2   L2
 /  \
L3  L4
```

LightGBM chooses to split the leaf that will result in the maximum decrease in loss.

#### Mathematical Formulation

At each iteration, LightGBM chooses to split the leaf $l^*$ that maximizes:

$$l^* = \arg\max_{l} \Delta \mathcal{L}(l)$$

Where $\Delta \mathcal{L}(l)$ is the reduction in loss from splitting leaf $l$.

### Python Implementation - Classifier - LightGBM

#### Installation

```bash
pip install lightgbm
```

#### Basic Implementation

```python
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

# Prepare your data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Create dataset for LightGBM
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

# Set parameters
params = {
    'objective': 'binary',           # binary classification
    'metric': 'binary_logloss',      # evaluation metric
    'boosting_type': 'gbdt',         # gradient boosting decision tree
    'num_leaves': 31,                # max number of leaves in one tree
    'learning_rate': 0.05,           # shrinkage rate
    'feature_fraction': 0.9,         # randomly select 90% of features
    'bagging_fraction': 0.8,         # randomly select 80% of data
    'bagging_freq': 5,               # perform bagging every 5 iterations
    'verbose': 0
}

# Train the model
model = lgb.train(
    params,
    train_data,
    num_boost_round=100,             # number of boosting iterations
    valid_sets=[train_data, val_data],
    valid_names=['train', 'valid'],
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

# Make predictions
y_pred_proba = model.predict(X_val, num_iteration=model.best_iteration)
y_pred = (y_pred_proba >= 0.5).astype(int)

# Evaluate
accuracy = accuracy_score(y_val, y_pred)
auc = roc_auc_score(y_val, y_pred_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"AUC-ROC: {auc:.4f}")
```

#### Using Scikit-learn API

```python
from lightgbm import LGBMClassifier

# Create classifier
clf = LGBMClassifier(
    objective='binary',
    num_leaves=31,
    learning_rate=0.05,
    n_estimators=100,
    random_state=42
)

# Fit the model
clf.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='logloss',
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

# Make predictions
y_pred = clf.predict(X_val)
y_pred_proba = clf.predict_proba(X_val)[:, 1]

# Evaluate
accuracy = accuracy_score(y_val, y_pred)
auc = roc_auc_score(y_val, y_pred_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"AUC-ROC: {auc:.4f}")
```

#### Multi-class Classification

```python
# For multi-class problems
params = {
    'objective': 'multiclass',
    'num_class': 3,                  # number of classes
    'metric': 'multi_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'verbose': 0
}

# Or using scikit-learn API
clf = LGBMClassifier(
    objective='multiclass',
    num_class=3,
    num_leaves=31,
    learning_rate=0.05,
    n_estimators=100
)
```

### Python Implementation - Regressor - LightGBM

```python
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Create regressor
reg = LGBMRegressor(
    objective='regression',
    num_leaves=31,
    learning_rate=0.05,
    n_estimators=100,
    random_state=42
)

# Fit the model
reg.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='rmse',
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

# Make predictions
y_pred = reg.predict(X_val)

# Evaluate
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"R²: {r2:.4f}")
```

#### Using Native API for Regression

```python
import lightgbm as lgb

# Create dataset
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

# Parameters
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'verbose': 0
}

# Train
model = lgb.train(
    params,
    train_data,
    num_boost_round=100,
    valid_sets=[val_data],
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

# Predict
y_pred = model.predict(X_val, num_iteration=model.best_iteration)
```

### Hyperparameter Tuning

#### Important Hyperparameters

**Tree Structure Parameters:**

- `num_leaves` (default=31): Maximum number of leaves in one tree
  - Larger values can increase accuracy but may cause overfitting
  - Should be less than $2^{\text{max\_depth}}$

- `max_depth` (default=-1): Maximum tree depth
  - -1 means no limit
  - Used to control overfitting

- `min_data_in_leaf` (default=20): Minimum number of samples in a leaf
  - Important for preventing overfitting

**Learning Control Parameters:**

- `learning_rate` (default=0.1): Shrinkage rate
  - Smaller values require more boosting rounds but may improve generalization
  - Typical range: [0.01, 0.3]

- `n_estimators` or `num_boost_round` (default=100): Number of boosting iterations
  - More trees can improve performance but increase training time
  - Use early stopping to find optimal value

**GOSS Parameters:**

- `top_rate` (default=0.2): Proportion of large gradient data to retain
- `other_rate` (default=0.1): Proportion of small gradient data to sample

**Feature Sampling:**

- `feature_fraction` (default=1.0): Randomly select a fraction of features
  - Can help prevent overfitting
  - Typical range: [0.5, 1.0]

**Bagging Parameters:**

- `bagging_fraction` (default=1.0): Randomly select a fraction of data
- `bagging_freq` (default=0): Frequency for bagging (0 means disabled)

#### Grid Search Example

```python
from sklearn.model_selection import GridSearchCV
from lightgbm import LGBMClassifier

# Define parameter grid
param_grid = {
    'num_leaves': [15, 31, 63],
    'max_depth': [3, 5, 7, -1],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [50, 100, 200],
    'min_child_samples': [10, 20, 30]
}

# Create model
lgb_model = LGBMClassifier(random_state=42)

# Grid search
grid_search = GridSearchCV(
    lgb_model,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

# Fit
grid_search.fit(X_train, y_train)

# Best parameters
print("Best parameters:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)
```

#### Optuna for Hyperparameter Optimization

```python
import optuna
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        'num_leaves': trial.suggest_int('num_leaves', 10, 100),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'random_state': 42
    }

    model = LGBMClassifier(**params)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc').mean()

    return score

# Create study
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Best parameters
print("Best parameters:", study.best_params)
print("Best score:", study.best_value)

# Train final model
best_model = LGBMClassifier(**study.best_params)
best_model.fit(X_train, y_train)
```

#### Practical Tips

1. **Start with default parameters** and use early stopping to find the right number of iterations.

2. **Tune `num_leaves` and `max_depth` first** as they have the most impact on model complexity.

3. **Reduce `learning_rate` and increase `n_estimators`** for better generalization.

4. **Use `feature_fraction` and `bagging_fraction`** to add randomness and prevent overfitting.

5. **Monitor validation metrics** during training to detect overfitting early.

6. **For large datasets**, consider using GOSS (`boosting_type='goss'`) for faster training.

7. **Handle categorical features** directly using `categorical_feature` parameter instead of one-hot encoding.

```python
# Example with categorical features
train_data = lgb.Dataset(
    X_train,
    label=y_train,
    categorical_feature=['category_col1', 'category_col2']
)
```
